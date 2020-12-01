# Predictive Model The Sound Transmission Loss (TL/STC) # 

Before walkthrough, Please read **Note** before,

## Get It !

### Initial Project 
```
pipenv shell 
pipenv install -r requirements.txt
```
### Testing
```
pytest 
```

### Example 
#### single_panel_run.py
```python

from model_tl_stc.single_panel import SinglePanel

if __name__ == '__main__':
    single_pn = SinglePanel(mass = 7, thick = 10, modulus = 4, damp = 0.1, width = 3, height = 4)
    single_pn.plot()
    data = single_pn.get_data()
    print("Transmission Loss (TL) for each frequency : \n")
    print(data)
    print("\n")
    print("Information of Panel : \n")
    info = single_pn.get_info()
    print(info)
```

#### double_panel_run.py
```python
from model_tl_stc.double_panel import DoublePanel
from model_tl_stc.single_panel import SinglePanel

if __name__ == '__main__':
    single_pn_a = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
    single_pn_b = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
    double_pn = DoublePanel(panel_a = single_pn_a, panel_b = single_pn_b, distance = 65, flow_res = 12000, spacing = 450)
    tl = double_pn.tl_panel_with_stud_and_absorber()
    double_pn.full_scale_plot(tl)
    double_pn.stc_scale_plot(tl)
    print("Transmission Loss (TL) for each frequency : \n")
    data = double_pn.get_data(tl)
    print(data)
    print("\n")
    print("Information of Panel : \n")
    info = double_pn.get_info(tl)
    print(info)
    print("Display data as Pandas DataFrame")
    print("\n")
    print(double_pn.get_data_pd(tl))
```
___

# Note


**This model used for study the predicting method of sound transmission loss.**  
The model used material property to estimate the sound transmission loss. Then evaluate by STC standard and visualization.   
• Reference Equation,formula from **Insul Document**  
• Document Reference :   
Jason Esan Cambridge (2006). Prediction tools for airborne sound insulation- evaluation and application. Department of Civil and  Environmental Engineering Division of Applied Acoustics, CHALMERS UNIVERSITY OF TECHNOLOGY, Sweden  

***FOR EDUCATION***    

# โมเดลการคาดคะเนค่าการสูญเสียพลังงานเสียงขณะส่งผ่านผนังและกำแพง #  
Repository นี้จัดทำเพื่อการศึกษา วิธีการคาดคะเน ค่าการสูญเสียพลังงานเสียงขณะส่งผ่านผนังและกำแพง ในรูปแบบชั้นเดียวและชั้นคู่ โดยอ้างอิงทฤษฎีการคาดคะเนจากข้อมูคุณสมบัติเฉพาะทางของวัสดุ เช่น มวล ค่าความยืดหยุ่น พื้นที่หน้าตัด เป็นต้น โมเดลนี้จะแสดงผลลัพธ์ในลักษณะของหน่วยวัดทาง Acoustics   
Transmission loss (TL) และทำการประเมินด้วยมาตรฐาน Sound Transmission loss (STC) โดยโมเดลนี้จะสามารถจัดรูปและแสดงผลลัพธ์ได้ในเชิง      
• กราฟ (Matplotlib)   
• ข้อมูลค่าพลังงานต่อความถี่ในรูป Dictionary และ table (pandas)     

**จัดทำเพื่อการศึกษาเท่านั้น**  

# Detail #

**Visulization**  

<img src="https://cdn-images-1.medium.com/max/1000/1*8ukywsj7mOJe_n_utts_ZQ.png" align ="bottom" height="320" width="600" ></img>


# Article (Thai Language) #  
<a href ="https://medium.com/@p.srinikorn/%E0%B8%A1%E0%B8%B2%E0%B8%A5%E0%B8%AD%E0%B8%87%E0%B9%83%E0%B8%8A%E0%B9%89-python-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B9%82%E0%B8%A1%E0%B9%80%E0%B8%94%E0%B8%A5-predict-%E0%B8%84%E0%B9%88%E0%B8%B2-sound-transmission-loss-tl-stc-afbf4b3ff150"> Medium Part 1 </a>   
<a href ="https://medium.com/@p.srinikorn/%E0%B8%A1%E0%B8%B2%E0%B8%A5%E0%B8%AD%E0%B8%87%E0%B9%83%E0%B8%8A%E0%B9%89-python-%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B9%82%E0%B8%A1%E0%B9%80%E0%B8%94%E0%B8%A5-predict-%E0%B8%84%E0%B9%88%E0%B8%B2-sound-transmission-loss-tl-stc-part-2-f79d184c97ad"> Medium Part 2 </a>    

<img src="https://cdn-images-1.medium.com/max/1000/1*D2U9IBPAclPUpZpH6GvBNA.jpeg" align ="bottom" height="380" width="600"></img>  
  
## Author : Peem Srinikorn 

