![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : 6TO4 | GRE | GRE6 | IP6IP6 | SIT
---------------------------------------------------------------
----------------------------------
![33399-icq-flower-logo-icon-vector-icon-vector-eps](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/9e736d80-9378-447d-a403-2ce0dacc3bec)
**توضیح کوتاه در مورد این پروژه :**

-----------------------


- 6TO4: encapsulates IPv6 packets within IPv4 packets for communication across IPv4 networks.

- GRE: (Generic Routing Encapsulation): Versatile tunneling protocol for encapsulating various network layer protocols, including IPv6, within IPv4 packets.

- GRE6: Variant of GRE specifically designed for tunneling IPv6 packets, simplifying their encapsulation within IPv4 packets.

- IP6IP6 (IPv6 over IPv6): Allows direct tunneling of IPv6 packets over an existing IPv6 infrastructure.

- SIT (Simple Internet Transition): Lightweight encapsulation method for tunneling IPv6 packets over an IPv4 infrastructure, requiring minimal configuration.
------------------------
![Update-Note--Arvin61r58](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/a149bfde-0f8f-44db-8360-0f9e9325983b) **اپدیت**

- مشکل ذخیره نکردن ایپی های جدید Native IPV6 حل شد
- کانفیگ سرور خارج و ایران باید سریع انجام شود. نخست سرور خارج را کانفیگ کنید و سپس سرور ایران را کانفیگ کنید.
- پس از uninstall قبل از انجام تانل های دیگر، یک بار هم ریبوت کنید.
--------------------------------

![R (a2)](https://github.com/Azumi67/RTT-Wireguard/assets/119934376/3f64bfa8-3785-4a0b-beba-366b3cb73719)
**دسترسی سریع به اسکریپت**


- [کلیک - click](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/blob/main/README.md#%D8%A7%D8%B3%DA%A9%D8%B1%DB%8C%D9%BE%D8%AA-%D9%85%D9%86)
------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات**
 <div dir="rtl">&bull;امکان تانل های متفاوت که شامل IP6IP6 | 6TO4 | GRE6 و غیره میشود.</div>
 <div dir="rtl">&bull;امکان پورت فوروارد و تانل اصلی پس از اجرای 6TO4 و سایر تانل ها</div>
 <div dir="rtl">&bull; امکان حذف جداگانه</div>
 <div dir="rtl">&bull; امکان تانل بدون داشتن Native IPV6</div>

 

![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/Haproxy_TCP_loadbalance/assets/119934376/a462de6d-be16-46dc-aaa8-c21a4c6df669)این پروژه آموزشی هست و خوشحال میشم اگر فیدبکی داشتید به من بگید که از آن برای یادگیری بیشتر استفاده کنم.لطفا اگر جایی اشتباه دیدید بگید که من هم بیشتر یاد بگیرم .thanks
- اگر میخواهید به چندین سرور تانل بزنید به [اینجا](https://github.com/Azumi67/6TO4-PrivateIP) مراجعه کنید

 
 ------------------------------------------------------
  
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش**

**روش IP6IP6**

----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 



 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/290ad745-cb6c-4634-a9c0-e6861ddbc084" alt="Image" />
</p>
 <div dir="rtl">&bull;کانفیگ را از سرور خارج شروع میکنیم </div>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید</div>


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/6127f7f5-d892-4cb1-8087-ed590a3834bc" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید</div>
        

  ![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1b367bc9-aaed-4a8d-84a6-a2a1fc31b831) 
  **سرویس پینگ و cronjob به صورت اتوماتیک اضافه خواهد شد**
  
  **اگر از پنل xui استفاده میکنید لطفا private ip range را باز بگذارید**



--------------------------------------
**روش GRE6**

--------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/756f468e-8d6c-45bd-9a4a-a9d056011147)**سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4b14b9da-c946-48ba-a1f5-c8259b59f9fd" alt="Image" />
</p>
 <div dir="rtl">&bull;کانفیگ را از سرور خارج شروع میکنیم </div>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید</div>

![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/590b11fa-f80f-4dc4-bedb-73746458f42b)**مثال**
- به طور مثال هم پنل در سرور ایران و خارج داریم. اول private ip range را باز میکنیم و سپس از ایپی های ساخته شده برای تانل یا پورت فوروارد استفاده میکنیم.
- به طور مثال برای dokodemo door از ایپی خارج که ساختیم استفاده میکنیم که اینجا 2002:831a::1 میباشد . پورت کانفیگ من در سرور خارج 8080 است و من همان پورت را برای سرور ایران قرار میدم.
- حالا به جای ادرس در کلاینت v2rayng از ایپی ورژن 4 سرور ایران و پورت انتخابی استفاده میکنیم
- برای همه تانل ها به همین صورت است. در gre6 به جای لوکال و ریموت از ایپی 6 استفاده شده است.

   
 ---------------------------------------
 
 ![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1b53f0b4-5338-444d-a0a3-a02d0ca6e431" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید</div>

        
  ![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1b367bc9-aaed-4a8d-84a6-a2a1fc31b831) 
  **سرویس پینگ و cronjob به صورت اتوماتیک اضافه خواهد شد**
  
  **اگر از پنل xui استفاده میکنید لطفا private ip range را باز بگذارید**
  
  ---------------------------------------

**روش GRE**

-------------------------------


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d63c344a-05c6-4218-84c2-21b6e9ed9c5b" alt="Image" />
</p>

 <div dir="rtl">&bull;کانفیگ را از سرور خارج شروع میکنیم </div>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید</div>


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d17bda7e-2d10-4de3-b76c-6af385492ddf" alt="Image" />
</p>

   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید</div>

--------------------------------------
**روش 6TO4**

-------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/87f554cb-1f40-475e-9737-a116ef6115dd" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید</div>


---------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/6de6acfa-6528-4c2d-bf26-e39dba8d05cd" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران و خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید</div>
          
------------------------------------------

**روش 6TO4 روت anycast**

-------------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/7bc82bd6-57dd-434f-83dd-a1b07221af8f" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید</div>


---------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1bffb577-88b8-4086-b70c-7aa3998098ae" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید</div>
          
---------------------------------

**اسکرین شات**
<details>
  <summary align="right">Click to reveal image</summary>
  
  <p align="right">
    <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8fabd39b-d38e-49ae-b26e-8f74f764e7d9" alt="menu screen" />
  </p>
</details>


------------------------------------------
![scri](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/cbfb72ac-eff1-46df-b5e5-a3930a4a6651)
**اسکریپت های کارآمد :**
- این اسکریپت ها optional میباشد.


 
 Opiran Script
```
apt install curl -y && bash <(curl -s https://raw.githubusercontent.com/opiran-club/VPS-Optimizer/main/optimizer.sh --ipv4)
```

Hawshemi script

```
wget "https://raw.githubusercontent.com/hawshemi/Linux-Optimizer/main/linux-optimizer.sh" -O linux-optimizer.sh && chmod +x linux-optimizer.sh && bash linux-optimizer.sh
```

<div dir="rtl">&bull; اضافه کردن ایپی 6 اضافه</div>
 
  
```
bash <(curl -s -L https://raw.githubusercontent.com/opiran-club/softether/main/opiran-seth)
```
-----------------------------------------------------
![R (a2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/716fd45e-635c-4796-b8cf-856024e5b2b2)
**اسکریپت من**
----------------


- اگر با دستوردوم نتوانستید اسکریپت را اجرا کنید، نخست دستور زیر را اجرا نمایید و سپس دستور اصلی اسکریپت را اجرا نمایید.(تنها زمانی این دستور را استفاده کنید که با دستور موفق به اجرای اسکریپت نشدید)

```
sudo apt-get install python-pip -y  &&  apt-get install python3 -y && alias python=python3 && python -m pip install colorama && python -m pip install netifaces
```
- سپس این دستور را اجرا نمایید.

```
apt install python3 -y && sudo apt install python3-pip &&  pip install colorama && pip install netifaces && apt install curl -y && python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipip.py --ipv4)
```
--------------------------------------
 <div dir="rtl">&bull;  دستور زیر برای کسانی هست که پیش نیاز ها را در سرور، نصب شده دارند</div>
 
```
python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipip.py --ipv4)
```
--------------------------------------
 <div dir="rtl">&bull; اگر سرور شما خطای externally-managed-environment داد از دستور زیر اقدام به اجرای اسکریپت نمایید.</div>
 
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/managed2.sh)"
```

---------------------------------------------
![R (7)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/42c09cbb-2690-4343-963a-5deca12218c1)
**تلگرام** 
![R (6)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/f81bf6e1-cfed-4e24-b944-236f5c0b15d3) [اپیران- OPIRAN](https://github.com/opiran-club)

---------------------------------
![R23 (1)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/18d12405-d354-48ac-9084-fff98d61d91c)
**سورس ها**


![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس های OPIRAN](https://github.com/opiran-club)

![R (9)](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4758a7da-ab54-4a0a-a5a6-5f895092f527)[سورس های Hwashemi](https://github.com/hawshemi/Linux-Optimizer)



-----------------------------------------------------

![youtube-131994968075841675](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/24202a92-aff2-4079-a6c2-9db14cd0ecd1)
**ویدیوی آموزش**

-----------------------------------------


