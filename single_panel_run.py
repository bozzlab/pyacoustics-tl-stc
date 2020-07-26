from model_tl_stc.single_panel import SinglePanel

if __name__ == '__main__':
    ### Attribute ##(mass, thick, modulus, damp, width, height): 
    single_pn = SinglePanel(mass = 7, thick = 10, modulus = 4, damp = 0.1, width = 3, height = 4)
    single_pn.plot()
    data = single_pn.get_data()
    print("Transmission Loss (TL) for each frequency : \n")
    print(data)
    print("\n")
    print("Information of Panel : \n")
    info = single_pn.get_info()
    print(info)