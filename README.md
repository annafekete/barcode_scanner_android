# barcode_scanner_android

Egy Androidos Zebra vonalkódleolvasóra fejleszteni egy Python-alapú alkalmazást, amely a beolvasott vonalkód alapján MySQL-adatbázisból lekérdezi, hogy létezik-e az adott termék, és ha igen, kihez tartozik, majd ezt az infót megjeleníti. Az adatbázis egy Apache szerveren fut, PHP-s API-n keresztül lehet lekérdezni az adatokat curl.exe segítségével, és a válasz JSON.
