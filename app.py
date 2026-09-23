import matplotlib

matplotlib.use("Agg")

import gradio as gr

from peak_ground_acceleration_estimator import (
    FAULT_CHOICES,
    SITE_CHOICES,
    estimate_pga,
    make_pga_chart,
)


def format_result(result):
    if result.get("error"):
        error = str(result["error"])
        return f'<span style="color:#c62828; font-weight:bold;">{error}</span>'

    pga_g = result["pga_g"]
    pga_cm_s2 = result["pga_cm_s2"]
    classification = result["classification"]
    color = result["color"]

    return (
        f"**Peak Ground Acceleration:** {pga_g:.3f} g  \n"
        f"**PGA (cm/s²):** {pga_cm_s2:.1f}  \n"
        f'**Classification:** <span style="color:{color}; font-weight:bold;">{classification}</span>'
    )


def run_estimator(magnitude, distance, site_class, fault_style):
    try:
        result = estimate_pga(magnitude, distance, site_class, fault_style)
        figure = make_pga_chart(result["pga_g"], result["error"], result["color"])
        return format_result(result), figure
    except Exception as exc:
        message = f"Unexpected error: {exc}"
        return (
            f'<span style="color:#c62828; font-weight:bold;">{message}</span>',
            make_pga_chart(0.0, message, "#666666"),
        )


with gr.Blocks(title="Peak Ground Acceleration Estimator") as demo:
    gr.Markdown(
        "# Peak Ground Acceleration Estimator\n"
        "Estimate PGA from an earthquake scenario using the Joyner & Boore (1981) "
        "attenuation relation with simplified site and faulting-style adjustments."
    )

    with gr.Row():
        with gr.Column(scale=1):
            magnitude = gr.Slider(
                minimum=3.0,
                maximum=9.0,
                value=6.5,
                step=0.1,
                label="Moment magnitude (M)",
            )
            distance = gr.Slider(
                minimum=0.1,
                maximum=500.0,
                value=50.0,
                step=0.1,
                label="Closest distance to fault rupture R (km)",
            )
            site_class = gr.Dropdown(
                choices=SITE_CHOICES,
                value=SITE_CHOICES[0],
                label="Site soil class",
            )
            fault_style = gr.Dropdown(
                choices=FAULT_CHOICES,
                value="Strike-slip",
                label="Faulting style",
            )
            estimate_button = gr.Button("Estimate PGA")

        with gr.Column(scale=1):
            result_output = gr.Markdown(
                "Enter an earthquake scenario and press **Estimate PGA**."
            )
            chart_output = gr.Plot()

    estimate_button.click(
        fn=run_estimator,
        inputs=[magnitude, distance, site_class, fault_style],
        outputs=[result_output, chart_output],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
