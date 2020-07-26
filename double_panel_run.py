from model_tl_stc.double_panel import DoublePanel
from model_tl_stc.single_panel import SinglePanel

if __name__ == '__main__':
    single_pn_a = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
    single_pn_b = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
    double_pn = DoublePanel(panel_a = single_pn_a, panel_b = single_pn_b, distance = 65, flow_res = 12000, spacing = 450)
    tl_with_stud_absorber = double_pn.tl_panel_with_stud_and_absorber()
    tl_with_stud = double_pn.tl_panel_and_stud()
    tl_with_absorber = double_pn.tl_panel_and_absorber()
    tl_double = double_pn.tl_double_panel()
    double_pn.full_scale_plot(tl_with_stud_absorber)
    double_pn.stc_scale_plot(tl_with_stud_absorber)
    print("Transmission Loss (TL) for each frequency : \n")
    data = double_pn.get_data(tl_with_stud_absorber)
    print(data)
    print("\n")
    print("Information of Panel : \n")
    info = double_pn.get_info(tl_with_stud_absorber)
    print(info)
    print("Display data as Pandas DataFrame")
    print("\n")
    print(double_pn.get_data_pd(tl_with_stud_absorber))