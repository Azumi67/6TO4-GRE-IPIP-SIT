![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : 6TO4 | GRE | GRE6 | IP6IP6 | SIT
---------------------------------------------------------------
----------------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات**

 
- امکان تانل های متفاوت که شامل IP6IP6 | 6TO4 | GRE6 و غیره میشود
- امکان پورت فوروارد و تانل اصلی پس از اجرای 6TO4 و سایر تانل ها
- امکان حذف جداگانه
- امکان تانل بدون داشتن Native IPV6
- اگر میخواهید به چندین سرور تانل بزنید به [اینجا](https://github.com/Azumi67/6TO4-PrivateIP) مراجعه کنید
- حتما پرایوت ایپی ها را در پنل باز کنید تا کانفیگ های شما کار کند.
- به زودی امکان تانل بین چند سرور در صورت امکان اضافه خواهم کرد.

 
 ------------------------------------------------------
<div align="right">
  <details>
    <summary><strong>توضیحات</strong></summary>
  
------------------------------------ 
- 6TO4: encapsulates IPv6 packets within IPv4 packets for communication across IPv4 networks.

- GRE: (Generic Routing Encapsulation): Versatile tunneling protocol for encapsulating various network layer protocols, including IPv6, within IPv4 packets.

- GRE6: Variant of GRE specifically designed for tunneling IPv6 packets, simplifying their encapsulation within IPv4 packets.

- IP6IP6 (IPv6 over IPv6): Allows direct tunneling of IPv6 packets over an existing IPv6 infrastructure.

- SIT (Simple Internet Transition): Lightweight encapsulation method for tunneling IPv6 packets over an IPv4 infrastructure, requiring minimal configuration.

  </details>
</div>

-----------------------
<div align="right">
  <details>
    <summary><strong>چند نکته در مورد خطا ها </strong></summary>
  
- اگز خطای buffer size گرفتید، اطمینان پیدا کنید که هر دو طرف سرور قبلا تانل 6to4 ای فعال ندارند.تانل بروکر هم پاک کنید
- اگر مشکلی در پینگ گرفتن داشتید، اطمینان پیدا کنید که ایپی ها را به درستی وارد کردید

  </details>
</div>

------------------------
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/3cfd920d-30da-4085-8234-1eec16a67460" alt="Image"> آپدیت</strong></summary>
  
------------------------------------ 

- چندین دستور ip اضافه شد
- از این به بعد میتوانید MTU را خودتان تنظیم کنید یا به صورت اتوماتیک مانند قدیم انتخاب شود.
- گرینه yes برای ست کردن Mtu به صورت دستی و گزینه no برای ست کردن اتوماتیک میباشد.
- اگر MTU مورد نظر شما ثبت نشد، هم سرور خارج و سرور ایران را یک بار ریبوت کنید.
- مشکل ذخیره نکردن ایپی های جدید Native IPV6 حل شد

  </details>
</div>

--------------------------------

  
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش**

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش IP6IP6</summary>
  
  
------------------------------------ 


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
  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش GRE6</summary>
  
  
------------------------------------ 

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

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش GRE</summary>
  
  
------------------------------------ 


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
  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4</summary>
  
  
------------------------------------ 

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

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4 روت anycast</summary>
  
  
------------------------------------ 


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
          <div dir="rtl">&bull;اگر سرور ایرانتون ایپی 6 داره میتونید با دستور روبرو از ایپی 6 anycast برای پکت های خروجی استفاده نمایید. ip -6 route replace default via fe80::1 dev eth0 src 2002:2bc.xxxx</div>
           <div dir="rtl">&bull;به جای eth0 از اینترفیس خودتان استفاده کنید و به جای 2002:2 bc هم از ایپی 6 خودتان که generate کردین استفاده کنید.</div>
  </details>
</div>

-------------------------------

**اسکرین شات**
<details>
  <summary align="right">Click to reveal image</summary>
  
  <p align="right">
    <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/40e01e48-64d9-4160-a6e9-545f4bde957d" alt="menu screen" />
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

-----------------------------------------------------
![R (a2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/716fd45e-635c-4796-b8cf-856024e5b2b2)
**اسکریپت من**
----------------

```
apt install python3 -y && sudo apt install python3-pip &&  pip install colorama && pip install netifaces && apt install curl -y && python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipip2.py --ipv4)
```


- اگر با دستور بالا نتوانستید اسکریپت را اجرا کنید، نخست دستور زیر را اجرا نمایید و سپس دستور اول را دوباره اجرا کنید.
- اگر باز هم colorama نصب نشد، دستور روبرو هم اجرا کنید .  pip3 install colorama

```
sudo apt-get install python-pip -y  &&  apt-get install python3 -y && alias python=python3 && python -m pip install colorama && python -m pip install netifaces
```
--------------------------------------
 <div dir="rtl">&bull;  دستور زیر برای کسانی هست که پیش نیاز ها را در سرور، نصب شده دارند</div>
 
```
python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipip2.py --ipv4)
```
--------------------------------------
 <div dir="rtl">&bull; اگر سرور شما خطای externally-managed-environment داد از دستور زیر اقدام به اجرای اسکریپت نمایید.</div>
 
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/managed2.sh)"
```

---------------------------------------------

![R23 (1)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/18d12405-d354-48ac-9084-fff98d61d91c)
**سورس ها**


![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس های OPIRAN](https://github.com/opiran-club)

![R (9)](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4758a7da-ab54-4a0a-a5a6-5f895092f527)[سورس های Hwashemi](https://github.com/hawshemi/Linux-Optimizer)



-----------------------------------------------------


