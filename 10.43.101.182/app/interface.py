import gradio as gr
import pandas as pd
import mlflow
from inference import (
    load_model_from_minio,
    make_prediction,
    get_latest_model,
    client
)

# Variable global del modelo
modelo = None  # Se cargará al usar la interfaz

# Función principal de predicción
def interfaz_prediccion(elevacion, pendiente):
    global modelo
    if modelo is None:
        return "⚠️ No hay modelo disponible para hacer predicciones.", None

    entrada = pd.DataFrame([{
        "feature1": elevacion,
        "feature2": pendiente
    }])

    resultado = make_prediction(modelo, entrada)

    model_name = get_latest_model()
    run_infos = client.search_model_versions(f"name='{model_name}'")
    if run_infos:
        run_id = run_infos[-1].run_id
        run = client.get_run(run_id)
        accuracy = run.data.metrics.get("accuracy", "N/A")
        return f"Predicción: {resultado['prediction']}", f"Modelo: {model_name} | Run ID: {run_id} | Precisión: {accuracy}"
    else:
        return f"Predicción: {resultado['prediction']}", "No se pudo obtener info del modelo"

# Lista los experimentos disponibles
def listar_experimentos():
    try:
        experiments = mlflow.search_experiments()
        if not experiments:
            return "No hay experimentos registrados."

        resumen = ""
        for exp in experiments:
            resumen += f"{exp.name} (ID: {exp.experiment_id})\n"
            resumen += f"  - Ubicación: {exp.artifact_location}\n"
            resumen += f"  - Estado: {exp.lifecycle_stage}\n\n"
        return resumen
    except Exception as e:
        return f"Error al obtener experimentos: {e}"

# Carga un modelo desde MinIO con run_id y artifact_path
def cargar_modelo_desde_minio(run_id, artifact_path):
    global modelo
    modelo = load_model_from_minio(run_id, artifact_path)
    if modelo is None:
        return "❌ Error al cargar el modelo desde MinIO."
    return f"✅ Modelo cargado correctamente desde run_id: {run_id}, path: {artifact_path}"

# Construcción de la interfaz con gr.Blocks
with gr.Blocks(title="Predicción") as app:
    gr.Markdown("## Predicción modelo cargado")

    with gr.Row():
        elev = gr.Number(label="Elevación")
        slope = gr.Number(label="Pendiente")

    btn_predecir = gr.Button("Predecir")
    resultado_prediccion = gr.Textbox(label="Resultado de la predicción")
    detalles_modelo = gr.Textbox(label="Detalles del modelo")

    btn_predecir.click(
        fn=interfaz_prediccion,
        inputs=[elev, slope],
        outputs=[resultado_prediccion, detalles_modelo]
    )

    gr.Markdown("---")
    gr.Markdown("### 🔎 Ver Experimentos Registrados")
    btn_exp = gr.Button("Ver Experimentos Registrados")
    caja_exp = gr.Textbox(label="Experimentos registrados", lines=10)
    btn_exp.click(fn=listar_experimentos, outputs=caja_exp)

    gr.Markdown("---")
    gr.Markdown("### 🔁 Cargar nuevo modelo desde MinIO")

    run_id_input = gr.Textbox(label="Run ID")
    artifact_input = gr.Textbox(label="Subcarpeta del modelo (artifact_path)", value="model")
    resultado_carga = gr.Textbox(label="Resultado de carga")

    btn_cargar = gr.Button("📦 Cargar modelo desde MinIO")
    btn_cargar.click(
        fn=cargar_modelo_desde_minio,
        inputs=[run_id_input, artifact_input],
        outputs=resultado_carga
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=8503)
