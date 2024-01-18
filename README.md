![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : anycast | 6TO4 | GRE | GRE6 | IP6IP6 | SIT
---------------------------------------------------------------
----------------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات و نکات**

 
- امکان تانل های متفاوت که شامل IP6IP6 | 6TO4 | GRE6 و غیره میشود
- امکان پورت فوروارد و تانل اصلی پس از اجرای 6TO4 و سایر تانل ها
- امکان حذف جداگانه
- امکان تانل بدون داشتن Native IPV6
- اگر میخواهید به چندین سرور تانل بزنید به [اینجا](https://github.com/Azumi67/6TO4-PrivateIP) مراجعه کنید
- امکان تغییر دیفالت روت هم اضافه شد برای کسانی که مشکل نوسان دارند.
- حتما پرایوت ایپی ها را در پنل باز کنید تا کانفیگ های شما کار کند.
- اگر در فایروال خود پرایوت ایپی ها را بستید، ایپی مربوطه را در فایروال خود باز کنید (اگر نمیدانید چگونه ! در اینترنت سرچ بکنید)
- امکان ویرایش MTU به menu اضافه شد (برای کاهش پکت لاست)
- به زودی امکان تانل بین چند سرور در صورت امکان اضافه خواهم کرد.

 
 ------------------------------------------------------
 <div align="right">
  <details>
    <summary><strong>نکات و خطاها </strong></summary>
  
- اگز خطای buffer size گرفتید، اطمینان پیدا کنید که هر دو طرف سرور قبلا تانل 6to4 ای فعال ندارند.تانل بروکر هم پاک کنید
- اگر مشکلی در پینگ گرفتن داشتید، اطمینان پیدا کنید که ایپی ها را به درستی وارد کردید
- لطفا دقت کنید در زمان حذف پرایوت ایپی به اشتباه گزینه اشتباه را انتخاب نکنید. این اسکریپت بارها تست شده است و به درستی باید کار کند.
- اگر پرایوت ایپی به درستی حذف نشود، تانل انجام نمیشود
- اگر در فایروال خود پرایوت ایپی ها را بستید، ایپی مربوطه را در فایروال خود باز کنید (اگر نمیدانید چگونه ! در اینترنت سرچ بکنید)
- اطمینان پیدا کنید که پرایوت ایپی ها را در پنل هم بلاک نکرده اید که تانل کار نخواهد کرد.
- اگر مسیر روت را تغییر دادید پس از انکه پاک کردید ، یک بار هم ریبوت نمایید.
- از edit mtu برای کاهش پکت لاست خود استفاده کنید. در هر دیتاسنتر میتواند متفاوت باشد.
- گزینه y به معنی تنظیم دستی mtu و گزینه n به معنی تنظیم اتوماتیک میباشد.

  </details>
</div>

------------------------
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
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/3cfd920d-30da-4085-8234-1eec16a67460" alt="Image"> آپدیت</strong></summary>
  
------------------------------------ 

- چندین دستور ip اضافه شد
- امکان replace route اضافه شد
- ویرایش mtu به منو اضافه شد
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
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/5bfbbea6-4543-48c1-a2f5-d6b617f7ebec" alt="Image" />
</p>

- سرور خارج را کانفیگ میکنیم.
- ایپی 4 خارج و ایران را میدهیم.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/ddf0ccf1-aa3d-45ec-ab8d-5a722cebc100" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- ایپی 4 خارج و ایران را میدهیم.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.
- اگر در ufw و یا هر فایروالی، ایپی پرایوت را بستید، این ایپی مورد نظر را در فایروال خود باز کنید.
- با دستور ip a میتوانید ایپی خود را مشاهده کنید.


  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش GRE6</summary>
  
  
------------------------------------ 

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/756f468e-8d6c-45bd-9a4a-a9d056011147)**سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/da16f215-2123-4976-90d3-36d132e71c6e" alt="Image" />
</p>

- سرور خارج را کانفیگ میکنیم.
- ایپی 4 خارج و ایران را میدهیم.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.


![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/590b11fa-f80f-4dc4-bedb-73746458f42b)**مثال**
- به طور مثال هم پنل در سرور ایران و خارج داریم. اول private ip range را باز میکنیم و سپس از ایپی های ساخته شده برای تانل یا پورت فوروارد استفاده میکنیم.
- به طور مثال برای dokodemo door از ایپی خارج که ساختیم استفاده میکنیم که اینجا 2002:831a::1 میباشد . پورت کانفیگ من در سرور خارج 8080 است و من همان پورت را برای سرور ایران قرار میدم.
- حالا به جای ادرس در کلاینت v2rayng از ایپی ورژن 4 سرور ایران و پورت انتخابی استفاده میکنیم
- برای همه تانل ها به همین صورت است. در gre6 به جای لوکال و ریموت از ایپی 6 استفاده شده است.

   
 ---------------------------------------
 
 ![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**



 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/ad3b01b5-5421-488a-9aa3-328773420d1c" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- ایپی 4 خارج و ایران را میدهیم.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.
- اگر در ufw و یا هر فایروالی، ایپی پرایوت را بستید، این ایپی مورد نظر را در فایروال خود باز کنید.
- با دستور ip a میتوانید ایپی خود را مشاهده کنید.

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

- کانفیگ را از سرور خارج شروع میکنیم
- ایپی 4 سرور ایران و خارج را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید
- در اینجا هم میتوانید مسیر روت را تغییر دهید و همچنین MTU را دستی ست نمایید

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d17bda7e-2d10-4de3-b76c-6af385492ddf" alt="Image" />
</p>

- ایپی 4 سرور ایران و خارج را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید
  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4</summary>
  
  
------------------------------------ 

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/bbe3e8ba-9b2d-4dec-a8dd-dce7345accf2" alt="Image" />
</p>

- ایپی 4 سرور ایران و خارج را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.


---------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**



<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/2a89cd90-af70-484c-b8fa-60bd3d08699e" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- ایپی 4 سرور ایران و خارج را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید و پکت لاست خود را با mtu های متفاوت بررسی کنید.
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.


  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4 روت anycast</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1c53419e-dcbe-43b5-aacf-570e0f2c37c6" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور خارج را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید</div>
          <div dir="rtl">&bull; اگر در تنظیم MTU اطلاعاتی ندارید، گزینه no را بزنید. بعدا ب!
رای کاهش پکت لاست میتوانید MTU را ویرایش کنید</div>
          
---------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1bffb577-88b8-4086-b70c-7aa3998098ae" alt="Image" />
</p>
   <div dir="rtl">&bull;ایپی 4 سرور ایران را وارد نمایید </div>
    <div dir="rtl">&bull; تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا</div>
        <div dir="rtl">&bull; از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید</div>
          <div dir="rtl">&bull; ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید</div>
          <div dir="rtl">&bull; اگر در تنظیم MTU آطلاعاتی ندارید، گزینه no را بزنید. بعدا برای کاهش پکت لاست میتوانید MTU را ویرایش کنید</div>
          <div dir="rtl">&bull; در صورت نوسان، مسیر روت را مانند من تغییر دهید. گزینه YES تغییر میدهد. اگر نوسانی ندارید میتوانید گزینه no را بزنید</div>
          
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
- برای بهبود عملکرد سرور میتوانید از optimizer استفاده نمایید.


 
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
apt install python3 -y && sudo apt install python3-pip &&  pip install colorama && pip install netifaces && apt install curl -y && python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipipv2.py --ipv4)
```


- اگر با دستور بالا نتوانستید اسکریپت را اجرا کنید، نخست دستور زیر را اجرا نمایید و سپس دستور اول را دوباره اجرا کنید.
- اگر باز هم colorama نصب نشد، دستور روبرو هم اجرا کنید .  pip3 install colorama

```
sudo apt-get install python-pip -y  &&  apt-get install python3 -y && alias python=python3 && python -m pip install colorama && python -m pip install netifaces
```
--------------------------------------
 <div dir="rtl">&bull;  دستور زیر برای کسانی هست که پیش نیاز ها را در سرور، نصب شده دارند</div>
 
```
python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ipipv2.py --ipv4)
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


