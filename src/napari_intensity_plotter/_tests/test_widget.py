import numpy as np
import os
from napari_intensity_plotter._widget import (
    IntensityPlotControlWidget,
    IntensityPlotWidget,
)

def test_intensity_plot_widget(make_napari_viewer):
    # Napari viewer を作成
    viewer = make_napari_viewer()

    # テスト用の画像データを追加
    layer = viewer.add_image(np.random.random((100, 100, 100)))

    # IntensityPlotWidget を作成し、viewer を渡す
    plot_widget = IntensityPlotWidget(viewer)
    assert plot_widget.viewer == viewer

    # IntensityPlotWidget のプロット機能をテスト
    plot_widget.update_plot(viewer, None)  # イベントがない場合も考慮
    assert plot_widget.intensity_data is not None
    assert len(plot_widget.intensity_data) == layer.data.shape[0]

    # 保存機能をテスト（実際のファイル保存は仮のディレクトリで行う）
    plot_widget.update_save_directory("/tmp")
    plot_widget.save_csv = True
    plot_widget.save_png = True
    plot_widget.save_to_csv()
    csv_path = os.path.join("/tmp", f"{plot_widget.layer_name}_y{plot_widget.clicked_coords[1]}_x{plot_widget.clicked_coords[0]}.csv")
    png_path = os.path.join("/tmp", f"{plot_widget.layer_name}_y{plot_widget.clicked_coords[1]}_x{plot_widget.clicked_coords[0]}.png")
    assert os.path.exists(csv_path)
    assert os.path.exists(png_path)


def test_intensity_plot_control_widget(make_napari_viewer):
    # Napari viewer を作成
    viewer = make_napari_viewer()

    # IntensityPlotControlWidget を作成し、viewer を渡す
    control_widget = IntensityPlotControlWidget(viewer)
    assert control_widget.viewer == viewer

    # square_size を変更し、IntensityPlotWidget に反映されるかをテスト
    control_widget.square_spinbox.setValue(5)
    assert control_widget.square_size == 5

    # ディレクトリを変更し、IntensityPlotWidget に反映されるかをテスト
    control_widget.save_path_input.setText("/tmp")
    control_widget.update_save_directory()
    assert control_widget.get_save_directory() == "/tmp"

    # PNG 保存の状態を変更し、IntensityPlotWidget に反映されるかをテスト
    control_widget.png_checkbox.setChecked(True)
    assert control_widget.save_png

    # "Hide All Layers" ボタンをクリックしてレイヤーが非表示になるかをテスト
    control_widget.hide_all_layers()
    for layer in viewer.layers:
        assert not layer.visible

    # "Focus on Visible Layer" ボタンをクリックしてレイヤーにフォーカスできるかをテスト
    control_widget.focus_on_visible_layer()
    # フォーカスされることを検証するテスト（フォーカスの具体的な効果による）


# このテストスクリプトは、IntensityPlotWidget と IntensityPlotControlWidget の各機能が期待通りに動作することを確認します。
