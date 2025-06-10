import sys
sys.path.append('../')

from pycore.tikzeng import *
from pycore.blocks import * 

# 定义网络结构
arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # 输入 (代表 I_0 ... I_N)
    to_Conv("input_frames", s_filer="256", n_filer=3, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, caption="Input I0..IN"),

    # ========== 左侧编码路径 (FFCMs) ==========
    to_Conv("l_ffcm1", s_filer="128", n_filer=64, offset="(2.5,0,0)", to="(input_frames-east)", width=4, height=30, depth=30, caption="FFCM 1"),
    to_connection("input_frames", "l_ffcm1"),

    to_Conv("l_ffcm2", s_filer="64", n_filer=128, offset="(3,0,0)", to="(l_ffcm1-east)", width=6, height=20, depth=20, caption="FFCM 2"),
    to_connection("l_ffcm1", "l_ffcm2"),

    to_Conv("l_ffcm3", s_filer="32", n_filer=256, offset="(3.5,0,0)", to="(l_ffcm2-east)", width=8, height=15, depth=15, caption="FFCM 3"),
    to_connection("l_ffcm2", "l_ffcm3"),

    to_Conv("l_ffcm4_bottleneck", s_filer="16", n_filer=512, offset="(4,0,0)", to="(l_ffcm3-east)", width=10, height=10, depth=10, caption="FFCM 4 (Bottleneck)"),
    to_connection("l_ffcm3", "l_ffcm4_bottleneck"),

    # ========== 右侧解码路径 (Upscale + BFCMs) ==========
    to_UnPool("up1", offset="(5,0,0)", to="(l_ffcm4_bottleneck-east)", width=1, height=15, depth=15, opacity=0.5, caption="Upscale"),
    to_Conv("r_bfcm1", s_filer="32", n_filer=256, offset="(0,0,0)", to="(up1-east)", width=8, height=15, depth=15, caption="BFCM 1"),
    to_connection("up1", "r_bfcm1"),
    to_skip(of="l_ffcm3", to="r_bfcm1", pos=1.25),

    to_UnPool("up2", offset="(3.5,0,0)", to="(r_bfcm1-east)", width=1, height=20, depth=20, opacity=0.5, caption="Upscale"),
    to_Conv("r_bfcm2", s_filer="64", n_filer=128, offset="(0,0,0)", to="(up2-east)", width=6, height=20, depth=20, caption="BFCM 2"),
    to_connection("up2", "r_bfcm2"),
    to_skip(of="l_ffcm2", to="r_bfcm2", pos=1.25),

    to_UnPool("up3", offset="(3,0,0)", to="(r_bfcm2-east)", width=1, height=30, depth=30, opacity=0.5, caption="Upscale"),
    to_Conv("r_bfcm3", s_filer="128", n_filer=64, offset="(0,0,0)", to="(up3-east)", width=4, height=30, depth=30, caption="BFCM 3"),
    to_connection("up3", "r_bfcm3"),
    to_skip(of="l_ffcm1", to="r_bfcm3", pos=1.25),

    to_UnPool("up4", offset="(2.5,0,0)", to="(r_bfcm3-east)", width=1, height=40, depth=40, opacity=0.5, caption="Upscale"),
    to_Conv("r_ffcm_final", s_filer="256", n_filer=32, offset="(0,0,0)", to="(up4-east)", width=2, height=40, depth=40, caption="Final FFCM"),
    to_connection("up4", "r_ffcm_final"),

    # 输出 (代表 O_0 ... O_N)
    # MODIFIED: 移除了 'n_filer' 参数
    to_ConvSoftMax("output_frames", s_filer="256", offset="(2.5,0,0)", to="(r_ffcm_final-east)", width=2, height=40, depth=40, caption="Output O0..ON" ),
    to_connection("r_ffcm_final", "output_frames"),

    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')
    print(f"Generated {namefile}.tex successfully.")

if __name__ == '__main__':
    main()