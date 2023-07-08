1) main.py dosyası, task'i çözdüğüm ana dosyadır. tüm kodlar yorum satırlarıyla açıklandı, düzgünce ve okunaklı yazıldı, işlem gücünü en az kullanacak şekilde yazmaya çalıştım, kullanabildiğim kadar fonksiyon kullanarak kodu olabildiğince modüler hale getirmeye ve özgür bırakmaya çalıştım.
2) main.py dosyası, move.py dosyasına bağımlılığa sahiptir, main dosyasını çalıştırmak için move.py ile aynı konumda olduğuna emin olunuz
3) move.py dosyası, aracın hareketlerini simüle edeceğim komut satırı print'lerini barındıran, bunları bir class içinde topladığım bir dosyadır.
4) main.py'de, inputtan alınan frame'ler ekrana bastırılmamaktadır. Görüntü işlemenin başarılı olduğunu görmek için, hiçbir bağımlılığı olmayan "cv_Show.py" dosyasını çalıştırınız.
5) hem main.py için, hem de cv_Show.py için, input dosyalarını elle atayacak şekilde ayarladım. her iki dosyanın da import kısmından hemen sonra, ilk değişken olarak "video" adında bir değişken bulunmaktadır. Bu değişkenin değerini string olacak şekilde video'nun yolu olarak değiştirdiğiniz taktirde çalışacaktır.
6) zamanınızı ayırdığınız için teşekkür ederim

Murathan Demir, EEF > EHB. 040210220.
