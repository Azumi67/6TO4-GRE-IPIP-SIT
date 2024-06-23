**این پروژه صرفا برای آموزش و بالا بردن دانش بوده است و هدف دیگری در ان نمیباشد**

**برای ubuntu24 از این کامند استفاده نمایید(برای سایر نسخه ها هم میتوانید استفاده کنید)** 
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ubuntu24.sh)"
```

**گزینه status اضافه و فیکس شد**

**اگر اسکریپت دیگری استفاده میکنید، لطفا بررسی کنید که دستورات من در crontab -e توسط اسکریپت دیگری حذف نشده باشد**

**تغییراتی در IPSEC انجام شد و encryption cryptographies تغییر کرد**


![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه :  Geneve | anycast | 6TO4 | GRE | GRE6 | IP6IP6 | SIT | Erspan + IPsec- چندین سرور ایران و خارج
---------------------------------------------------------------
----------------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات و نکات**

- دارای گزینه Status و نوع تانل شما و تعداد سرور آنلاین در هر سرور و ایپی ریموت سرور شما را نشان میدهد.
- امکان تانل های متفاوت که شامل IP6IP6 | 6TO4 | GRE6 | Geneve | Erspan + IPsec و غیره میشود
- امکان تانل 6TO4 و ANYCAST و IP6IP6 و GRE6 بین چندین سرور خارج و ایران
- امکان پورت فوروارد و تانل اصلی پس از اجرای 6TO4 و سایر تانل ها
- امکان تانل بین 5 سرور ایران و ده سرور خارج
- امکان تانل vxlan به صورت تک سرور به صورت three methods
- امکان تانل Geneve با چندین روش متفاوت (مولتی سرور و به صورت تکی)
- امکان تانل Geneve با IPsec ( مولتی و تکی)
- امکان تانل erspan همراه با ipsec ( مدل ساده آن بر بستر ایپی ورژن ۴ بر روی بعضی سرور های ایران کار نمیکند)
- امکان تانل gre6tap به صورت تکی و مولتی همراه با ipsec
- تانل Geneve +  Gre6 با دو روش NATIVE یا IPV4
- امکان حذف جداگانه
- امکان تانل بدون داشتن Native IPV6
- امکان تغییر دیفالت روت هم اضافه شد برای کسانی که مشکل نوسان دارند.
- حتما پرایوت ایپی ها را در پنل باز کنید تا کانفیگ های شما کار کند.
- اگر در فایروال خود پرایوت ایپی ها را بستید، ایپی مربوطه را در فایروال خود باز کنید (اگر نمیدانید چگونه ! در اینترنت سرچ بکنید)
- امکان ویرایش MTU به menu اضافه شد (کاهش packet loss)
---------------
- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید و حتما پس از روشن کردن آن، ufw reload هم بزنید اگر کار نکرد**
- **اگر فایروال روشن دارید و تانل gen کار نکرد، پس از هر بار ریبوت ممکن است نیاز باشد که یک بار بر روی هر دو سرور ufw reload بزنید وگرنه ممکن است تانل کار نکند.**
- **اگر یک روش کار نکرد روش های دیگر را امتحان کنید.**(اگر بعضی روش ها کار نکرد ، پس از uninstall، یک بار هم ریبوت نمایید)
- **در 6to4 روش anycast و بدون anycast احتمال از کار افتادن native میباشد و باید default route را فعال کنید**
-------

  <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/3cfd920d-30da-4085-8234-1eec16a67460" alt="Image"> آپدیت</strong></summary>
  
------------------------------------ 

- گزینه Status اضافه شد و نوع تانل شما و تعداد سرور آنلاین در هر سرور و ایپی ریموت سرور شما را نشان میدهد.(فیکس شد)
- آموزش Vxlan برای تک سرور قرار داده شد.
- تغییراتی در روت gre6, gre6tap و تمام Ipsec ها و تک سرور ها و پنج سرور ایران و 10 خارج انجام شد.
- ایپی اضافه برای Ipsec حذف شد از انجا که در داخل ecryption loop نبود.
- راهنمای نام اینترفیس و تانل به منوهای مربوطه اضافه شد Tunnel names guide
- ویرایش سرور اضافه شد
- 5 سرور ایران و 10 سرور خارج ( روش sit) اضافه شد
- ده سرور خارج اضافه شد
- محاسبه اتومات MTU به دلیل فاکتورهای زیاد و سرور های متنوع، حذف شد
- اضافه شدن ipsec به همه تانل ها
- اضافه شدن Geneve به همراه IPsec ( مولتی و تک سرور)
- اضافه شدن Gre6tap به همراه IPsec (روش های مختلف)
- اضافه شدن پنج سرور به IP6IP6 و Gre6
- تانل erspan همراه با ipsec اضافه شد
- مشکلات کار نکردن تانل ip6tnl بعد از ریبوت، برطرف شد
- مشکلات mtu در private ip چندین سرور برطرف شد
- مشکلات تنظیم دیفالت روت و MTU برطرف شد
- اضافه کردن گزینه روت برای gre6 + native gen
- تانل geneve با چندین روش متفاوت اضافه شد
- امکان تانل بین چندین سرور اضافه شد.
- چندین دستور ip اضافه شد
- امکان replace route اضافه شد
- ویرایش mtu به منو اضافه شد
- از این به بعد میتوانید MTU را خودتان تنظیم کنید یا به صورت اتوماتیک مانند قدیم انتخاب شود.
- گرینه yes برای ست کردن Mtu به صورت دستی و گزینه no برای ست کردن اتوماتیک میباشد.
- مشکل ذخیره نکردن ایپی های جدید Native IPV6 حل شد

  </details>
</div>

--------------------------------

 <div align="right">
  <details> 
    <summary><strong><img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/aa529e70-6eec-46bd-bec0-50fb1d9a4aa5" alt="Image"> نکات و خطا ها (مهم)</strong></summary>

- اگر خطای buffer size گرفتید، اطمینان پیدا کنید که هر دو طرف سرور قبلا تانل 6to4 ای فعال ندارند.
- اگر مشکلی در پینگ گرفتن داشتید، اطمینان پیدا کنید که ایپی ها را به درستی وارد کردید
- لطفا دقت کنید در زمان حذف پرایوت ایپی به اشتباه گزینه اشتباه را انتخاب نکنید. این اسکریپت بارها تست شده است و به درستی باید کار کند.
- اگر پرایوت ایپی به درستی حذف نشود، تانل انجام نمیشود
- اگر در فایروال خود پرایوت ایپی ها را بستید، ایپی مربوطه را در فایروال خود باز کنید (اگر نمیدانید چگونه ! در اینترنت سرچ بکنید)
- اطمینان پیدا کنید که پرایوت ایپی ها را در پنل هم بلاک نکرده اید که تانل کار نخواهد کرد.
- از edit mtu برای کاهش پکت لاس خود استفاده کنید. در هر دیتاسنتر میتواند متفاوت باشد.
- گزینه y به معنی تنظیم دستی mtu و گزینه n به معنی تنظیم اتوماتیک میباشد.
- مطمئن شوید که اسکریپت های دیگر، دستورات کرون من را پاک نمیکند وکرنه تانل از کار میوفتد.
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

- Geneve : (Generic Network Virtualization Encapsulation) is a network tunneling protocol that provides a mechanism for encapsulating and decapsulating network packets for virtualized environments. It is designed to enable efficient network virtualization and overlay network solutions in cloud computing, data centers, and software-defined networking (SDN) environments.

Geneve is an extension of the original Virtual Extensible LAN (VXLAN) protocol and addresses certain limitations of VXLAN. It provides enhanced scalability, extensibility, and flexibility for network virtualization. Geneve encapsulates the original network packets inside a new tunneling header, allowing these packets to traverse an underlay network while being associated with specific virtual networks or tenants.

  </details>
</div>

-----------------------
 ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش ویرایش سرور**
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4  | ایپی پرایوت 6</summary>
    
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج و ایران** 



- **من دو سرور خارج دارم و یک سرور ایران و میخوام یک سرور اضافه کنم**
- برای تمامی روش ها قابلیت ویرایش اضافه شده است و این آموزش، تنها دو بخش را توضیح میدهد.
- دقت کنید در اینجا سروری نیازی نیست که پاک شود. برای پاک کردن و اضافه کردن به قسمت بعدی مراجعه کنید که توضیح دادم.
- در سرور خارج، وارد گزینه edit servers میشوم و داخل گزینه  6to4 > 10 kharej 1 iran وارد میشوم. سپس گزینه خارج سوم را میزنم و سرور سوم خارج را اضافه میکنم.
- حالا اسکریپت را در سرور ایران اجرا میکنم و وارد گزینه edit servers میشوم و سپس وارد گزینه 6to4 < 10 kharej 1 iran میشوم
- گزینه 10 سرور خارج 1 سرور ایران را انتخاب میکنم و سپس گزینه 11 یعنی سرور ایران را انتخاب میکنم
- سرور سوم را انتخاب میکنم تا سرور سوم در ایران اضافه شود

------------------

  </details>
</div>  
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4 IPSEC  | ایپی پرایوت 6</summary>
    
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج و ایران** 



- **من سه سرور خارج دارم و یک سرور ایران و میخواهم سرور سوم را پاک کنم و دوباره اضافه کنم**
- وارد گزینه edit servers میشوم و گزینه Remove را انتخاب میکنم و داخل گزینه 6to4 IPsec وارد میشوم. سپس گزینه خارج سوم را میزنم و سرور سوم خارج را پاک میکنم.
- حالا اسکریپت را در سرور ایران اجرا میکنم و وارد گزینه edit servers میشوم و گزینه remove را انتخاب میکنم و سپس وارد گزینه 6to4 ipsec میشوم.
- گزینه 5 سرور خارج 1 سرور ایران را انتخاب میکنم و سپس گزینه 6 یعنی سرور ایران را انتخاب میکنم
- سرور سوم را انتخاب میکنم تا سرور سوم در ایران حذف شود.
- در اینجا از ما سوال میشود که سرور های ما هم اکنون چند تا است. چون یک سرور پاک کردیم پس 2 سرور خارج داریم.عدد 2 و secret key پیشین خود را وارد نمایید. اینکار برای reconfig ipsec میباشد
- حالا باید در سرور های خارج systemctl restart strong-azumi1 را وارد کنم.
- سپس هم در سرور خارج و هم در سرور ایران سرور سوم خارج را اضافه میکنم. بدین صورت میشود
- در سرور خارج، وارد گزینه edit servers > add > 6to4 ipsec > 5 kharej 1 iran میشوم. خارج سوم رو انتخاب میکنم
- حالا در سرور ایران، وارد گزینه edit servers > add > 6to4 ipsec > 5 kharej 1 iran میشوم . گزینه 6 یعنی سرور ایران را انتخاب میکنم و سرور سوم خارج را اضافه میکنم.

------------------

  </details>
</div>  

-------------------------------------

  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش تک سرور**
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>مشاهده tunnel status </summary>
  
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **تک سرور** 

 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/0444ddb8-bcc2-48bb-82d9-3db4f6797cd9" alt="Image" />
</p>

- از این به بعد میتوانید secret key در صورت نصب ipsec هم مشاهده کنید و نام اینترفیس و نام تانل در اسکریپت که بتوانید به سادگی حذفش نمایید
- در این اسکرین من Private + IPsec را کانفیگ کردم و مشاهده میکنید که کاملا مشخص هست که کدام تانل کانفیگ شده است

------------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Vxlan با IPsec به صورت P2P</summary>
  
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 

 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/c3402f06-c441-4b1e-b18b-0d60d73201d7" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های Vxlan، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- **حتما ufw reload را پس از اتمام کانفیگ در صورت داشتن فایروال، اجرا کنید**
- در این آموزش روش Vxlan P2P به همراه IPsec را به شما نشان میدهم.
- این تانل به صورت point to point میباشد و نیاز به وارد کردن ایپی سرور خارج و سرور ایران میباشد. این تانل میتواند هم با IPsec و هم بدون IPsec باشد
- سرور خارج را کانفیگ میکنیم. من ایپی لوکال آخر را میخواستم به صورت private ip 6 باشد. شما میتوانید گزینه private ipv4 را انتخاب کنید
- ایپی 4 ایران و خارج را وارد میکنم
- پورت مقصد را 5513 وارد میکنم. شما میتوانید هر پورتی بدهید.
- سکرت کی را ازومی وارد میکنم. شما میتوانید به صورت generate شده وارد نمایید( در هر دو طرف سرور باید یکسان باشد)
- پس از نصب ipsec از من سوال میشود که ایا میخواهید که خود اسکریپت، اینترفیس اصلی را پیدا کند ؟ من y را وارد کردم . شما میتوانید به صورت دستی وارد نمایید. به طور مثال ممکن است اینترفیس اصلی شما eth0 یا ens و یا سایر موارد باشد( این مورد گاهی اوقات به کار می آید و وجودش نیاز بوده است)
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- رول های فایروال به صورت خودکار اضافه میشود.


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/81758945-23a7-4e7a-b65d-d7e7120d36c9" alt="Image" />
</p>

- مانند کانفیگ سرور خارج پیش میروم.چون در سرور خارج، private ip به صورت ipv6 میباشد باید در این سرور هم به صورت private ipv6 باشد.
- سرور ایران را کانفیگ میکنیم.
- ایپی 4 ایران و خارج را وارد میکنم
- پورت را مانند سرور خارج عدد 5513 قرار میدهم
- سکرت کی را مانند سرور خارج، ازومی قرار میدهم.
- پس از نصب ipsec، از من سوال میشود که ایا میخواهم خود اسکریپت اینترفیس اصلی را پیدا کند یا به صورت manual وارد میکنم ؟ من y را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- رول های فایروال اضافه شد
- یادتان باشد که در صورت داشتن فایروال حتما ufw reload را بزنید که پینگ شما فعال شود( بهتر است کانفیگ را بدون فایروال انجام دهید و پس از روشن کنید)
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Vxlan بدون IPsec به صورت FDB</summary>
  
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/b5f2a189-aec7-4c57-bd5e-2248e7c5d81e" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های Vxlan، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- **حتما ufw reload را پس از اتمام کانفیگ در صورت داشتن فایروال، اجرا کنید**
- در این آموزش روش Vxlan FDB بدون IPsec را به شما نشان میدهم. با IPsec هم به همین صورت میباشد تنها با توجه به اینکه نیاز به وارد کردن secret key دارید.
- این تانل به صورت FDB و با Bridge میباشد و نیاز به وارد کردن ایپی سرور Remote میباشد. این تانل میتواند هم با IPsec و هم بدون IPsec باشد
- سرور خارج را کانفیگ میکنیم.من ایپی لوکال آخر را میخواستم به صورت private ip 6 باشد. شما میتوانید گزینه private ipv4 را انتخاب کنید
- ایپی 4 ایران را وارد میکنم
- پورت مقصد را 5513 وارد میکنم. شما میتوانید هر پورتی بدهید.
- پس از نصب bridge از من سوال میشود که ایا میخواهید که خود اسکریپت، اینترفیس اصلی را پیدا کند ؟ من y را وارد کردم . شما میتوانید به صورت دستی وارد نمایید. به طور مثال ممکن است اینترفیس اصلی شما eth0 یا ens و یا سایر موارد باشد( این مورد گاهی اوقات به کار می آید و وجودش نیاز بوده است)
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- رول های فایروال به صورت خودکار اضافه میشود.


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/c6069b15-33bd-4653-8c36-b349c35c4d9b" alt="Image" />
</p>

- مانند کانفیگ سرور خارج پیش میروم.چون در سرور خارج، private ip به صورت ipv6 میباشد باید در این سرور هم به صورت private ipv6 باشد.
- سرور ایران را کانفیگ میکنیم.
- ایپی 4 خارج را وارد میکنم (سرور remote)
- پورت را مانند سرور خارج عدد 5513 قرار میدهم
- پس از نصب bridge، از من سوال میشود که ایا میخواهم خود اسکریپت اینترفیس اصلی را پیدا کند یا به صورت manual وارد میکنم ؟ من y را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- رول های فایروال اضافه شد
- یادتان باشد که در صورت داشتن فایروال حتما ufw reload را بزنید که پینگ شما فعال شود( بهتر است کانفیگ را بدون فایروال انجام دهید و پس از روشن کنید)
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Vxlan با Bridge & IP بدون IPsec</summary>
  
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 

 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/ddd7c796-dabd-43ae-9bbf-dc2ea9c61915" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های Vxlan، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- **حتما ufw reload را پس از اتمام کانفیگ در صورت داشتن فایروال، اجرا کنید**
- در این آموزش روش Vxlan With Bridge & IP بدون IPsec را به شما نشان میدهم. با IPsec هم به همین صورت میباشد تنها با توجه به اینکه نیاز به وارد کردن secret key دارید.
- این تانل به صورت دادن Remote IP input و با Bridge میباشد و نیاز به وارد کردن ایپی سرور Remote میباشد. این تانل میتواند هم با IPsec و هم بدون IPsec باشد
- سرور خارج را کانفیگ میکنیم.من ایپی لوکال آخر را میخواستم به صورت private ip 4 باشد. شما میتوانید گزینه private ipv6 را انتخاب کنید
- ایپی 4 ایران را وارد میکنم یا همون سرور remote را وارد میکنم
- پورت مقصد را 5513 وارد میکنم. شما میتوانید هر پورتی بدهید.
- پس از نصب bridge از من سوال میشود که ایا میخواهید که خود اسکریپت، اینترفیس اصلی را پیدا کند ؟ من y را وارد کردم . شما میتوانید به صورت دستی وارد نمایید. به طور مثال ممکن است اینترفیس اصلی شما eth0 یا ens و یا سایر موارد باشد( این مورد گاهی اوقات به کار می آید و وجودش نیاز بوده است)
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- برای mtu دو مورد برای کانفیگ خواهیم داشت. یک مورد برای vxlan device و یکی هم برای bridge. من به صورت manual هر دو mtu را وارد کردم. شما میتوانید به صورت خودکار انتخاب کنید.
- رول های فایروال به صورت خودکار اضافه میشود.


----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d0bff3b4-a5ed-4588-90af-e9b76c6bd4e9" alt="Image" />
</p>

- مانند کانفیگ سرور خارج پیش میروم
- سرور ایران را کانفیگ میکنیم.چون در سرور خارج، private ip به صورت ipv4 میباشد باید در این سرور هم به صورت private ipv4 باشد.
- ایپی 4 خارج را وارد میکنم (سرور remote)
- پورت را مانند سرور خارج عدد 5513 قرار میدهم
- پس از نصب bridge، از من سوال میشود که ایا میخواهم خود اسکریپت اینترفیس اصلی را پیدا کند یا به صورت manual وارد میکنم ؟ من y را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- برای mtu دو مورد برای کانفیگ خواهیم داشت. یک مورد برای vxlan device و یکی هم برای bridge. من به صورت manual هر دو mtu را وارد کردم. شما میتوانید به صورت خودکار انتخاب کنید.
- رول های فایروال اضافه شد
- یادتان باشد که در صورت داشتن فایروال حتما ufw reload را بزنید که پینگ شما فعال شود( بهتر است کانفیگ را بدون فایروال انجام دهید و پس از روشن کنید)
------------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + GRE6 | ایپی پرایوت 4</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 



 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/c9d176d3-56ca-42a4-88c4-729c98effd45" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- ایپی 4 ایران و خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- مسیر اصلی default route را تغییر میدهم. شما میتوانید اینکار را نکنید.
 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/00f6eb28-194c-4cd8-9cde-f55229f81749" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- رول های فایروال اضافه شد تا ارتباط برقرار شود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4c8edc1c-89ac-474c-9696-cf676e5df508" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- ایپی 4 ایران و خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- مسیر اصلی default route را تغییر میدهم. شما میتوانید اینکار را نکنید.
 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d56b7258-6249-4776-9cf5-06451e88e0fb" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- رول های فایروال اضافه شد تا ارتباط برقرار شود

------------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + IPSEC | ایپی پرایوت 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 



 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/e6d39d8f-340c-4656-a3e7-14021bf491ff" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- دقت نمایید برای IPSEC من از گزینه GENEVE ADDRESS استفاده میکنم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- برای SECRET KEY میتوانید مانند من از AZUMI یا به صورت رندوم generate نمایید . باید در هر دو سرور مقدار یکسانی قرار بدید
- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- رول های فایروال اضافه شد تا ارتباط برقرار شود
- دقت نمایید این روش مانند سایرروش ها ممکن است در بعضی از دیتاسنتر ها بسته باشد و به منظور باگ برنامه و خرابی روش نیست.

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/bb138b35-946f-41ef-a902-e0b907ebf5f1" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- دقت نمایید برای IPSEC من از گزینه GENEVE ADDRESS استفاده میکنم
- ایپی 4 ایران و خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- برای SECRET KEY میتوانید مانند من از AZUMI یا به صورت رندوم generate نمایید . باید در هر دو سرور مقدار یکسانی قرار بدید
- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- رول های فایروال اضافه شد تا ارتباط برقرار شود

------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + NATIVE + GRE6 | ایپی پرایوت 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8a1255fb-f5f7-49d9-9023-492beeb332f8" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- چون میخواهم ایپی پرایوت من از نوع 6 باشد در قسمت GENEVE IP VERSION ، گزینه دوم ایپی 6 رو انتخاب میکنم تا ایپی پرایوت 6 به من بدهد
- ایپی 6 ایران و خارج را وارد میکنم. اگر سرور ایران شما، ایپی 6 ندارد... میتوانید از تانل بروکر هم استفاده نمایید.
- اگر ایپی 6 سرور خارج شما مناسب نبود میتوانید از EXTRA NATIVE IP، یک ایپی 6 دیگر برای سرور خارجتان بگیرید و از ان استفاده نمایید.
- اگرنمی دانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/b972a5c4-d2b7-4b98-af13-6190b9080f25" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- برای پینگ سرویس، ایپی 4 سرور ایران را بدهید.
- رول های فایروال اضافه شد تا ارتباط برقرار شود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/29d78e09-9d7d-4b07-a2d3-ff4cc507f47a" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- در سرور خارج در قسمت GENEVE IP VERSION از ایپی 6 استفاده کردیم پس در سرور ایران هم از ایپی 6 استفاده میکنیم.
- ایپی 6 ایران و خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1f6f4810-05f2-44e2-9557-556d178c2ae5" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- برای پینگ سرویس، ایپی 4 سرور ایران را بدهید.
- رول های فایروال اضافه شد تا ارتباط برقرار شود

------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + NATIVE + IP6TNL + GRE6 | ایپی پرایوت 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8ff505d6-93e2-40fb-bf3d-b159eca45bf9" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- چون میخواهم ایپی پرایوت من از نوع 6 باشد در قسمت GENEVE IP VERSION ، گزینه دوم ایپی 6 رو انتخاب میکنم تا ایپی پرایوت 6 به من بدهد
- ایپی 6 ایران و خارج را وارد میکنم. اگر سرور ایران شما، ایپی 6 ندارد... میتوانید از تانل بروکر هم استفاده نمایید.
- اگر ایپی 6 سرور خارج شما مناسب نبود میتوانید از EXTRA NATIVE IP، یک ایپی 6 دیگر برای سرور خارجتان بگیرید و از ان استفاده نمایید.
- اگرنمی دانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4259352e-9a5a-425e-b41f-067543e90d7c" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- برای پینگ سرویس، ایپی 4 سرور ایران را بدهید.
- رول های فایروال اضافه شد تا ارتباط برقرار شود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/a3c23960-8f23-436f-ba16-001d98fc58cb" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنیم.
- در سرور خارج در قسمت GENEVE IP VERSION از ایپی 6 استفاده کردیم پس در سرور ایران هم از ایپی 6 استفاده میکنیم.
- ایپی 6 ایران و خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/99170117-c5b9-4a22-9cbf-eca477fb6812" alt="Image" />
</p>

- برای geneve تنظیم mtu رو به صورت اتوماتیک انتخاب میکنم. شما میتوانید گزینه yes را بزنید و به صورت دستی وارد نمایید.
- کانفیگ انجام شد و ایپی نهایی به شما نمایش داده میشود
- برای پینگ سرویس، ایپی 4 سرور ایران را بدهید.
- رول های فایروال اضافه شد تا ارتباط برقرار شود

------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve Method 2 | پرایوت ایپی 4</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 



 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/a07b5e50-73d5-444e-af0d-56038a39b101" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب میکنم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/ee26ca1e-faf9-4b27-a00a-f42c09c2958d" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب کردیم
- ایپی 4  ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve Method 2 | پرایوت ایپی 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/b67cee71-ad77-4223-9f9f-086503ccb8b4" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب میکنم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور ایران را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/57ded48c-3972-4f5b-b6e1-17b794197af2" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب کردیم
- ایپی 4 سرور خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور خارج را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve Method 1 | پرایوت ایپی 4</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/30851e2f-4b26-4b90-97af-6a17eca1f8d0" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب میکنم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/9a7de8d9-d362-420b-b475-c98261f1e0cf" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب کردیم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve Method 1 | پرایوت ایپی 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 


 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/6c0d0159-4ee6-4959-86d7-51237256c632" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب میکنم
- ایپی 4 ایران را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور ایران را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/fe62d05f-2b5c-4d44-94f2-724530eea3df" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب کردیم
- ایپی 4 خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور خارج را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + Native | پرایوت ایپی 4</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 

 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/e5aabf75-d238-42f7-874e-461893c88746" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب میکنم
- ایپی 6 ایران را وارد میکنم. میتوانید از طریق تانل بروکر، ایپی 6 بگیرید و ان را وارد کنید یا اگر سرور شما ایپی 6 دارد ، ان را وارد کنید. (اتصال شما به خوب بودن و نداشتن اختلال بر روی این ایپی 6، بستگی دارد)
- اگر ایپی 6 سرور خارج شما مناسب نبود میتوانید از EXTRA NATIVE IP، یک ایپی 6 دیگر برای سرور خارجتان بگیرید و از ان استفاده نمایید.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور ایران را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/735da7cf-3cdf-4e98-87f0-04796fa27fb3" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 4 را انتخاب کردیم
- ایپی 6 خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور خارج را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Geneve + Native | پرایوت ایپی 6</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج** 

 <p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/44496990-8b3f-44e2-9a41-61515b616bf4" alt="Image" />
</p>

- **حتما برای کانفیگ تانل های geneve، نخست فایروال ufw را خاموش کنید و پس از اتمام کانفیگ میتوانید روشن نمایید**
- سرور خارج را کانفیگ میکنیم.
- در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب میکنم
- ایپی 6 ایران را وارد میکنم. میتوانید از طریق تانل بروکر، ایپی 6 بگیرید و ان را وارد کنید یا اگر سرور شما ایپی 6 دارد ، ان را وارد کنید. (اتصال شما به خوب بودن و نداشتن اختلال بر روی این ایپی 6، بستگی دارد)
- اگر ایپی 6 سرور خارج شما مناسب نبود میتوانید از EXTRA NATIVE IP، یک ایپی 6 دیگر برای سرور خارجتان بگیرید و از ان استفاده نمایید.
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور ایران را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده شما در آخر به شما نمایش داده میشود

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/49000de2-53b6-4c5c-888d-f1f397d77b92)**سرور ایران**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8337f2ef-6dcc-4300-8be4-07aa0842d00f" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنیم.
- در سرور خارج و در قسمت GENEVE IP VERSION ، پرایوت ایپی 6 را انتخاب کردیم
- ایپی 6 خارج را وارد میکنم
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- ایپی 4 سرور خارج را برای سرویس پینگ وارد میکنم.
- ایپی ساخته شده در اخر به شما نمایش داده میشود.
------------------

  </details>
</div>

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
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
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
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.
- اگر در ufw و یا هر فایروالی، ایپی پرایوت را بستید، این ایپی مورد نظر را در فایروال خود باز کنید.
- با دستور ip a میتوانید ایپی خود را مشاهده کنید.

------------------

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
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
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
- اگرنمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.
- و هم چنین دوباره گزینه No را برای ست کردن mtu، انتخاب میکنم. اگر آگاهی کافی دارید، mtu مناسب خود را بیابید.
- اگر در ufw و یا هر فایروالی، ایپی پرایوت را بستید، این ایپی مورد نظر را در فایروال خود باز کنید.
- با دستور ip a میتوانید ایپی خود را مشاهده کنید.
------------------

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
------------------

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
- اگر نمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
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
- اگر نمیدانید چه mtu مناسب شما هست گزینه No رو بزنید. بعدا میتوانید در منو آن را ویرایش کنید
- تعداد ایپی اضافه هم یک عدد وارد میکنم
- اگر نوسانی ندارید میتوانید مسیر روت را تغییر ندهید. برای این آموزش من مسیر روت را تغییر دادم.
- اگر مسیر روت را تغییر داد و میخواهید این تانل را پاک کنید ، سرور هایتان را پس از پاک کردن ، یک بار ریبوت هم بکنید.

------------------

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

- ایپی 4 سرور خارج را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور ایران را برای فعال کردن سرویس پینگ وارد نمایید
- اگر در تنظیم MTU اطلاعاتی ندارید، گزینه no را بزنید که به صورت اتوماتیک ست شود
          
---------------------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/5207faf2-3d0f-43dc-90a7-9ea14c536d40" alt="Image" />
</p>

- ایپی 4 سرور ایران را وارد نمایید
- تعداد ایپی مورد نیاز خود را وارد نمایید. به طور مثال 2 تا
- از ایپی های generate شده برای تانل استفاده نمایید یا با دستور ip a، ایپی های ساخته شده را ببینید
- ایپی ادرس 4 سرور خارج را برای فعال کردن سرویس پینگ وارد نمایید
- اگر در تنظیم MTU آطلاعاتی ندارید، گزینه no را بزنید.
-  در صورت نوسان، مسیر روت را مانند من تغییر دهید. گزینه YES تغییر میدهد. اگر نوسانی ندارید میتوانید گزینه no را بزنید   
 </details>
</div>

-------------------------------
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش مولتی سرور** 
- این اسکریپت بارها توسط من تست شده است. اگر اموزش کمی سخت بود بر روی سرور تست، آزمون و خطا کنید
- نمیتونستم اسکریپت رو ساده تر از این بکنم و با این حال احساس میکنم ممکن است کمی در نگاه اول، سخت باشد.
----------------

  </details>
</div>  
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش Sit بین 2 سرور خارج و 2 سرور ایران</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج اول**



<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1cf836a1-df0d-496d-b72a-fe398efb73ab" alt="Image" />
</p>

- نخست از Engboy تشکر میکنم به خاطر ایده ایشان که باعث شد کانفیگ منو ها و این روش ساده تر شود.
- خب من 2 سرور خارج و 2 سرور ایران دارم و میخواهم از طریق Sit این تانل را برقرار کنم
- نخست سرور خارج اول را کانفیگ میکنم. در این سرور ما باید دو بار کانفیگ انجام دهیم. یک بار برای سرور اول ایران و بار دیگر برای سرور دوم ایران.
- حالا وارد گزینه 3 به عبارتی کانفیگ 5 ایران و 10 خارج میشوم. سپس وارد PRIVATE[SIT] میشوم و گزینه اول یعنی خارج اول را انتخاب میکنم.
- نخست از ما سوال میشود که چند سرور ایران داریم. من دو سرور ایران دارم پس عدد 2 را وارد میکنم.
- ایپی 4 سرور اول خارج و سرور اول ایران را وارد میکنم.
- تعداد ایپی اضافه را یک وارد میکنم و mtu را گزینه نه میزنم. میتوانید همینجا هم یک mtu دلخواه قرار دهید
<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/6d0a3faf-2e79-4683-8974-e4cf49e1be51" alt="Image" />
</p>

- سپس کانفیگ بعدی شروع میشود. حالا ما باید سرور دوم ایران را در سرور خارج اول کانفیگ کنیم
- ایپی سرور اول خارج و ایپی سرور دوم ایران را وارد میکنم
- دقت کنید که اشتباه ایپی ها را وارد نکنید که باعث کار نکردن کانفیگ شما میشود. سرورهایتان را در notepad با شماره گذاری مشخص کنید
- نام اینترفیس ها هم در سرور ایران و خارج به دلیل ان که سردرگم نشوید، یکسان انتخاب شده است .
- نام های اینترفیس به این صورت میباشد iran2config5 = این به این معنی است که ایران دوم و کانفیگ (خارج) سوم . اینطوری شما میتوانید بفهمید که کدام سرور را کانفیگ کرده اید
- نگران این خطا RTNETLINK answers: File exists نباشید

---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/6f9a34e8-7e0b-4dc2-ab08-ab4f7d9e3163" alt="Image" />
</p>

- سرور خارج دوم را کانفیگ میکنم
- ایپی 4 سرور دوم خارج و سرور اول ایران را وارد میکنم.
- تعداد ایپی اضافه را یک قرار میدهم و mtu رو وارد میکنم یا گزینه نه را میزنم و بعدا وارد میکنم.
<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/306eb7b8-e8ea-4b8d-bc5c-82a156fb50a3" alt="Image" />
</p>
- حالا نوبت کانفیگ دوم در سرور دوم خارج میباشد
- ایپی سرور دوم خارج و سرور دوم ایران را وارد میکنم.(این کانفیگ سرور دوم خارج هست که دو عدد سرور ایران را در آن میخواهم کانفیگ کنم)

---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور اول ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d8cdc049-bdb5-48ad-8284-a02bcba2a754" alt="Image" />
</p>

- سرور اول ایران را کانفیگ میکنم
- از همان صفحه مربوط به کانفیگ privateip[Sit] گزینه 11 که iran servers میشود را انتخاب میکنم
- سپس از من سوال میشود گه کدام سرور ایران را میخواهم کانفیگ کنم. من سرور اول ایران را میخواهم کانفیگ کنم. پس عدد یک را وارد میکنم
- سپس از من میپرسد که چه تعداد سرور خارج دارم. من 2 عدد سرور خارج دارم
- دقت نمایید که در هر سرور ایران میشود ده سرور خارج اضافه کرد و در هر سرور خارج میشود 5 سرور ایران اضافه کرد.
- کانفیگ سرور اول آغاز میشود و ایپی 4 سرور اول ایران و سرور اول خارج را وارد میکنم.
<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8466e599-f2c5-4c5d-9cf0-a7cb59929bfa" alt="Image" />
</p>

- چون دو عدد سرور خارج دارم پس باید در سرور اول ایران دو بار کانفیگ را برای سرور های مختلف خارج، انجام دهم.
- ایپی سرور دوم خارج و سرور اول ایران را وارد میکنم.
- تعداد ایپی اضافه را 1 انتخاب میکنم
- باید الان به هر دو سرور در صورت درستی کانفیگ، پینگ را نمایش دهد. در غیر اینصورت یا به درستی کانفیگ نکردید یا پرایوت ایپی در سرور شما بسته میباشد
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور دوم ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/2603c32b-bd82-4583-97d9-28520915f111" alt="Image" />
</p>

- سرور دوم ایران را کانفیگ میکنم
- از همان صفحه مربوط به کانفیگ privateip[Sit] گزینه 11 که iran servers میشود را انتخاب میکنم
- سپس از من سوال میشود گه کدام سرور ایران را میخواهم کانفیگ کنم. من سرور دوم ایران را میخواهم کانفیگ کنم. پس عدد 2 را وارد میکنم
- سپس از من میپرسد که چه تعداد سرور خارج دارم. من 2 عدد سرور خارج دارم
- دقت نمایید که در هر سرور ایران میشود ده سرور خارج اضافه کرد و در هر سرور خارج میشود 5 سرور ایران اضافه کرد.
- کانفیگ سرور دوم ایران آغاز میشود و ایپی 4 سرور دوم ایران و اول خارج را وارد میکنم.
<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/231f82ed-9377-4ecb-aadd-bbc88df33a63" alt="Image" />
</p>

- چون دو عدد سرور خارج دارم پس باید در سرور دوم ایران هم دو بار کانفیگ را برای سرور های مختلف خارج، انجام دهم.
- ایپی سرور دوم خارج و سرور دوم ایران را وارد میکنم.
- تعداد ایپی اضافه را 1 انتخاب میکنم
- باید الان به هر دو سرور در صورت درستی کانفیگ، پینگ را نمایش دهد. در غیر اینصورت یا به درستی کانفیگ نکردید یا پرایوت ایپی در سرور شما بسته میباشد

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **نحوه پاک کردن**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d7994223-7011-4c00-9285-d262176f81b7" alt="Image" />
</p>

- به طور مثال میخواهم کانفیگ های سرور ایران را در سرور خارج پاک کنم. سرور خارج را انتخاب میکنم .
- از من پرسیده میشود که لیست کدام سرور خارج را برای پاک کردن کانفیگ ها میخوام. من سرور اول را میخواهم
- دقت نمایید در هر سرور خارج میشود پنچ کانفیگ سرور ایران را انجام داد. چون 5 سرور ایران و 10 سرور خارج در این تانل شدنی است.
- منوی سرور اول خارج میاید و کانفیگ ها را به صورت نام دقیق اینترفیس نشان میدهد. به طور مثال میخوام سرور دوم ایران در سرور اول خارج را پاک کنم. نام اینترفیس iran2config1 میشود. این گزینه را انتخاب و پاک میکنم. اگر میخواهم سرور دوم خارج را پاک کنم باید داخل لیست دوم، اینکار را انجام دهم .
- اگر به طور مثال لیست سرور دوم خارج را میخواهم، باید زمانی که از من سوال میشود، عدد 2 را وارد کنم که لیست سرور دوم خارج را برای من بیاورد
  
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **نحوه ویرایش سرور**

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/421c008c-9b9a-41d8-ae5a-118baf48526c)" alt="Image" />
</p>

- من میخواهم ویرایشی در سرور اول ایران انجام دهم. مثلا در سرور اول ایران میخواهم کانفیگ سرور سوم خارج را اضافه کنم
- گزینه ایران را وارد میکنم و سپس از من سوال میشود که کدام سرور ایران را میخواهم ادیت کنم. عدد 1 را وارد میکنم
- لیست ویرایش سرور برای سرور اول ایران باز میشود
- باید بر اساس نام اینترفیس، سرور سوم خارج را در سرور اول ایران اضافه کنید. سرور اول ایران و سرور سوم خارج ، نام اینترفیسش میشود iran1config3
- خب این گزینه را انتخاب میکنم و کانفیگ انجام میشود. حالا دوباره ویرایش سرور را در سرور سوم خارج انجام میدهم. هنگامی که از من سوال شد که کدام سرور خارج ؟ من عدد 3 را وارد میکنم تا لیست ویرایش سرور برای سرور سوم خارج باز شود
- سپس باید بر اساس نام اینترفیس، سرور اول ایران در سرور سوم خارج کانفیگ نمایم. سرور اول ایران سرور سوم خارج نام اینترفیسش میشود iran1config3 
- این گزینه iran1config3 را انتخاب میکنم و کانفیگ انجام میشود و در صورت درستی انجام آن باید پینگ دریافت کنید
- اگر مقداری این موارد سخت بود ، با آزمون و خطا این مشکل برطرف میشود.
---------------
 </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش IP6IP6 IPSEC  | ایپی پرایوت 6</summary>
    
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج و ایران** 



- **من دو سرور خارج دارم و یک سرور ایران و میخواهم بوسیله IP6IP6 و IPSEC تانل را برقرار کنم**
- وارد گزینه IP6IP6 + IPSEc میشوم و گزینه 5 خارج و یک ایران را انتخاب میکنم.
- سرور اول و دوم خارج را کانفیگ میکنم و عدد MTU مناسب را وارد میکنم
- در سرور ایران تعداد سرور خارج را 2 انتخاب میکنم و هر دو سرور را کانفیگ میکنم و عدد MTU مناسب را وارد میکنم
- دقت کنید که اسکریپت های دیگر باعث از بین رفتن کامند های من در کرون نشود که باعث از بین رفتن تانل پس از ریبوت و از کار افتادن ریست تایمر IPSEC میشود.
- ریست تایمر IPSEC بهتر است بین 2 تا 5 دقیقه باشد و میتوانید از طریق گزینه ویرایش در خود IP6IP6 + IPSEC ، این مقدار را وارد نمایید
- دقت نمایید از ایپی اضافه (ایپی پرایوت دوم) برای پورت فوروارد یا تانل استفاده ننمایید و تنها از ایپی نخستین خود در تانل یا پورت فوروارد استفاده نمایید( بعدا قابلیت ایپی اضافه برای ipsec حذف خواهد شد){در اپدیت جدید ، ایپی اضافه برای Ipsec حذف شد}
- با این دستور سرویس موردنظر systemctl restart strong-azumi1 ریست میشود.

------------------

  </details>
</div>  

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش IP6IP6 بین 3 سرور خارج و 1 سرور ایران</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/427104fe-0e38-4f87-a15c-387fbf10d3c1" alt="Image" />
</p>

- خب من 2 سرور خارج و 1 سرور ایران دارم و میخواهم از طریق IP6IP6 این تانل را برقرار کنم
- نخست سرور خارج اول را کانفیگ میکنم
- ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4db46ac0-fac0-4086-8e48-9fad2e7e7e0f" alt="Image" />
</p>

- سرور خارج دوم را کانفیگ میکنم
- ایپی 4 سرور دوم خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/229a0767-705a-4782-b55a-f628f7d34dd5" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنم
- نخست از من میپرسد که چه تعداد سرور خارج دارم. من 2 عدد سرور خارج دارم
- کانفیگ سرور اول آغاز میشود و ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.
<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/0bd168a7-6b2b-4561-84b2-0bd84ee5c283" alt="Image" />
</p>

- کانفیگ سرور دوم آغاز میشود و ایپی 4 سرور دوم خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------

 </details>
</div>
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش IP6IP6 بین 3 سرور ایران و 1 سرور خارج</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/b1d391f9-06da-4fcd-81f7-7390e006e0d3" alt="Image" />
</p>

- خب من 2 سرور ایران و 1 سرور خارج دارم و میخواهم از طریق IP6IP6 این تانل را برقرار کنم
- نخست سرور خارج را کانفیگ میکنم
- از من سوال میشود چند سرور ایران دارم ، من 2 عدد سرور ایران دارم پس عدد 2 را وارد میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/5eb12947-727f-4cfd-853f-cf628a49f7dc" alt="Image" />
</p>

- ادامه کانفیگ را انجام میدم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/72ea230e-0a1f-4b1c-9978-0de598f8ae67" alt="Image" />
</p>

- سرور ایران اول را کانفیگ میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/cafd52b7-6802-4359-bd61-731ed1a0a409" alt="Image" />
</p>

- سرور ایران دوم را کانفیگ میکنم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس دوباره از من میخواهد که IP6IP6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------

 </details>
</div>
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش GRE6 بین 3 سرور خارج و 1 سرور ایران</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/85e4985a-161d-43b3-9314-afed32e49e84" alt="Image" />
</p>

- خب من 2 سرور خارج و 1 سرور ایران دارم و میخواهم از طریق GRE6 این تانل را برقرار کنم
- نخست سرور خارج اول را کانفیگ میکنم
- ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که  GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d0b25c30-4fcb-49ae-aaec-328983b6c828" alt="Image" />
</p>

- سرور خارج دوم را کانفیگ میکنم
- ایپی 4 سرور دوم خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4e265f17-22fc-4520-bdbe-ec783632bf55" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنم
- نخست از من میپرسد که چه تعداد سرور خارج دارم. من 2 عدد سرور خارج دارم
- کانفیگ سرور اول آغاز میشود و ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d8165985-da76-4659-9a81-2c9b009902e2" alt="Image" />
</p>

- کانفیگ سرور دوم آغاز میشود و ایپی 4 سرور دوم خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------

 </details>
</div>
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش GRE6 بین 3 سرور ایران و 1 سرور خارج</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/851dd5d3-624a-4993-af2d-5e4eea861e08" alt="Image" />
</p>

- خب من 2 سرور ایران و 1 سرور خارج دارم و میخواهم از طریق GRE6 این تانل را برقرار کنم
- نخست سرور خارج را کانفیگ میکنم
- از من سوال میشود چند سرور ایران دارم ، من 2 عدد سرور ایران دارم پس عدد 2 را وارد میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/99b82ecd-b02d-4d2a-94d4-d69143cce8f8" alt="Image" />
</p>

- ادامه کانفیگ را انجام میدم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/563653c9-f1b3-4128-9bd4-5aa4bccf50ab" alt="Image" />
</p>

- سرور ایران اول را کانفیگ میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/cafd52b7-6802-4359-bd61-731ed1a0a409" alt="Image" />
</p>

- سرور ایران دوم را کانفیگ میکنم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس دوباره از من میخواهد که GRE6 MTU را تنظیم کنم
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.

 ---------------------------------------
 
 </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4 بین 5 سرور خارج و 1 سرور ایران</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8ad6ffa8-b9f4-449c-9cbe-c6b8442a5306" alt="Image" />
</p>

- خب من 2 سرور خارج و 1 سرور ایران دارم و میخواهم از طریق 6TO4 این تانل را برقرار کنم
- نخست سرور خارج اول را کانفیگ میکنم
- ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/0e463162-0184-4f2d-96d6-c0fd4cf0c849" alt="Image" />
</p>

- سرور خارج دوم را کانفیگ میکنم
- ایپی 4 سرور دوم خارج را وارد میکنم.
- تعداد ایپی اضافه را 1 انتخاب میکنم
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/a17229b0-a725-45e4-b2ef-387528d8bc56" alt="Image" />
</p>

- سرور ایران را کانفیگ میکنم
- نخست از من میپرسد که چه تعداد سرور خارج دارم. من 2 عدد سرور خارج دارم
- کانفیگ سرور اول آغاز میشود و ایپی 4 سرور اول خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/08de50f2-4cef-4321-949d-072fc31c85fd" alt="Image" />
</p>

- کانفیگ سرور دوم آغاز میشود و ایپی 4 سرور دوم خارج را وارد میکنم.
- ایپی 4 سرور ایران را وارد میکنم ( ایپی سرور ایران برای تمامی سرور های خارج یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------

 </details>
</div>
<div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش 6TO4 بین 5 سرور ایران و 1 سرور خارج</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/8b1b1310-a218-47a1-ae94-31c90d679d66" alt="Image" />
</p>

- خب من 2 سرور ایران و 1 سرور خارج دارم و میخواهم از طریق 6TO4 این تانل را برقرار کنم
- نخست سرور خارج را کانفیگ میکنم
- از من سوال میشود چند سرور ایران دارم ، من 2 عدد سرور ایران دارم پس عدد 2 را وارد میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس ایپی های GENERATE شده برای سرور اول را میتوانید مشاهده کنید.

<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4fff1f7d-ec19-4c8c-a0e5-19eff01aeffa" alt="Image" />
</p>

- ادامه کانفیگ را انجام میدم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم ( ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- سپس ایپی های GENERATE شده برای سرور دوم را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/d771b747-6046-4a1e-a1b1-f85e5a5df925" alt="Image" />
</p>

- سرور ایران اول را کانفیگ میکنم
- ایپی 4 سرور اول ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/21a4e1bd-878a-4297-af6a-cac38488eabc" alt="Image" />
</p>

- سرور ایران دوم را کانفیگ میکنم
- ایپی 4 سرور دوم ایران را وارد میکنم.
- ایپی 4 سرور خارج را وارد میکنم (ایپی سرور خارج برای تمامی سرور های ایران یکسان است)
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- تعداد ایپی اضافه را 1 انتخاب میکنم
- در سرور ایران default route را تغییر میدهم پس گزینه yes رو میزنم . شما میتوانید گزینه No را بزنید.
- سپس ایپی های GENERATE شده را میتوانید مشاهده کنید.
---------------

 </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>روش ANYCAST پنج سرور خارج و ایران</summary>

---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران اول**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/92314ffc-71b6-4317-9a4c-3580414935e9" alt="Image" />
</p>

- خب من 2 سرور ایران و 1 سرور خارج دارم و میخواهم از طریق این روش، این تانل را برقرار کنم
- شما میتوانید 3 سرور ایران و 3 سرور خارج را کانفیگ کنید. در اینجا برای اموزش صرفا از 2 سرور ایران و یک ایپی خارج استفاده میکنم. لطفا آموزش را با دقت بخوانید.
- نخست سرور ایران اول را کانفیگ میکنم
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- مسیر دیفالت روت را در سرور ایران تغییر میدهم پس گزینه YES را انتخاب میکنم.
- من 3 سرور دارم. در حال حاضر داخل سرور اول ایران هستم.از من سوال میشود که چه تعداد سرور دارم ( این سوال برای سرویس پینگ است). پس باید دو سرویس پینگ برای دو سرور دیگر درست کنم. پس عدد 2 را وارد میکنم که 2 عدد سرویس پینگ ایجاد شود
- ایپی 4 ادرس سرور های دیگر را وارد میکنم. پس ایپی ادرس سرور ایران دوم و ایپی ادرس سرور خارج را وارد میکنم. همین کار باید در سرور های دیگر هم انجام شود وگرنه ممکن است به مشکل بخورید.
- با دستور ip a میتوانید ایپی های generate شده را ببینید.
---------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور ایران دوم**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/748ab862-a94c-4b63-ac29-b2f81a70df8c" alt="Image" />
</p>


- سرور ایران دوم را کانفیگ میکنم
- ایپی 4 سرور ایران دوم را وارد میکنم.
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- مسیر دیفالت روت را در سرور ایران تغییر میدهم پس گزینه YES را انتخاب میکنم.
- من 3 سرور دارم. در حال حاضر داخل سرور دوم ایران هستم.از من سوال میشود که چه تعداد سرور دارم ( این سوال برای سرویس پینگ است). پس باید دو سرویس پینگ برای دو سرور دیگر درست کنم. پس عدد 2 را وارد میکنم که 2 عدد سرویس پینگ ایجاد شود
- ایپی 4 ادرس سرور های دیگر را وارد میکنم. پس ایپی ادرس سرور ایران اول و ایپی ادرس سرور خارج را وارد میکنم. همین کار باید در سرور های دیگر هم انجام شود وگرنه ممکن است به مشکل بخورید.
- با دستور ip a میتوانید ایپی های generate شده را ببینید.
---------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/c14c77ec-dc4e-4c8a-bdc2-4dc4e42a1815) **سرور خارج**


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/325512ab-351b-478d-b446-4aed2ee702fb" alt="Image" />
</p>


- سرور خارج را کانفیگ میکنم
- ایپی 4 سرور خارج را وارد میکنم.
- سپس میتوانم گزینه Y را بزنم و MTU را به صورت دستی وارد نمایم یا گزینه N را بزنم و به صورت AUTO این کار انجام شود. بعدا میتوانید MTU را در منو اسکریپت ویرایش نمایید
- من 3 سرور دارم. در حال حاضر داخل سرور خارج هستم.از من سوال میشود که چه تعداد سرور دارم ( این سوال برای سرویس پینگ است). پس باید دو سرویس پینگ برای دو سرور دیگر درست کنم. پس عدد 2 را وارد میکنم که 2 عدد سرویس پینگ ایجاد شود
- ایپی 4 ادرس سرور های دیگر را وارد میکنم. پس ایپی ادرس سرور ایران اول و ایپی ادرس سرور ایران دوم را وارد میکنم. همین کار باید در سرور های دیگر هم انجام شود وگرنه ممکن است به مشکل بخورید.
- با دستور ip a میتوانید ایپی های generate شده را ببینید.

---------------

 </details>
</div>
 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>نحوه ویرایش mtu</summary>

---------------



<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/13c54935-60d5-42cd-801a-ba5092a44a45" alt="Image" />
</p>

- برای نمونه من میخواهم mtu دو تانلی 6to4 ای که در سرور خارج ساختم را ویرایش کنم. نخست وارد قسمت ویرایش Mtu میشوم و کانفیگ 5 سرور ایران و 1 سرور خارج را انتخاب میکنم
- سپس سرور خارج را انتخاب میکنم. حالا در این منو میتوانم 5 تانل 6to4 که درست کرده ام را ویرایش کنم . من دو سرور ایران داشتم پس 2 تانل در سرور خارج درست شده است
- میتوانم به صورت جداگانه mtu این تانل ها را ویرایش کنم یا به صورت دست جمعی
- به طور مثال mtu تانل سرور اول و دوم را میتوانم به صورت جداگانه ویرایش کنم . اما در این آموزش من به صورت دست جمعی را نشان میدهم. بقیه را خودتان ازمون و خطا کنید.
- پس گزینه all of them را انتخاب میکنم و تعداد سرور ایران هم 2 وارد میکنم که در سرور خارج دو تانل 6to4 ایجاد شده را ویرایش کنم
- برای سرور اول mtu انتخابی خود را قرار میدم و سپس همینکار را برای سرور دوم انجام میدم
- به این صورت شما میتوانید به سادگی mtu های تانل ها و سرور های خود را ویرایش کنید.
- دقت نمایید که در مسیر مربوطه بروید و به اشتباه تانل دیگر را ویرایش نکنید
- دقت نمایید که سرور های خود را بدانید که کدام به کدام است و اشتباه ویرایش نکنید.
---------------

 </details>
</div>


 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>نحوه پاک کردن</summary>

---------------


<p align="right">
  <img src="https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/56b75075-4012-4c2e-928c-3fad2d9fc984" alt="Image" />
</p>

- برای نمونه من میخواهم سرویس و ایپی های ایجاد شده برای gre6 را پاک کنم. تانل من 3 سرور ایران و یک سرور خارج میباشد و میخواهم در سرور خارج عملیات پاک کردن را انجام بدهم.
- نخست وارد گزینه gre6 میشوم و گزینه 3 سرور ایران و 1 سرور خارج را انتخاب میکنم.
- گزینه 4 سرور خارج را انتخاب میکنم.
- از من سوال میشود که چه تعداد سرور ایران دارم. من دو عدد داشتم پس عدد 2 را وارد میکنم
- سپس تمامی سرویس ها و ایپی ها پاک میشود
- دقت نمایید که در مسیر درست هستید وگرنه عملیات پاک کردن به درستی انجام نمیشود.
 </details>
</div>

---------------
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

Kalilovers Script [for ipsec]
```
python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
```
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
- برای ubuntu24 از این دستور استفاده نمایید
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/6TO4-GRE-IPIP-SIT/main/ubuntu24.sh)"
```

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



