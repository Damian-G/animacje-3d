// parametry i pojedyncze wskazowki
class Wskazowka {
    constructor(dlugosc, grubosc, kolor) {
        this.dlugosc = dlugosc;
        this.grubosc = grubosc;
        this.kolor = kolor;
    }

    //pojedyncza wskazowka
    rysuj(ctx, kat) {
        ctx.save();
        ctx.rotate(kat);
        ctx.beginPath();
        ctx.lineWidth = this.grubosc;
        ctx.strokeStyle = this.kolor;
        ctx.lineCap = "round";
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -this.dlugosc);
        ctx.stroke();
        ctx.restore();
    }
}

class Zegar {
    constructor(idCanvasa) {
        this.canvas = document.getElementById(idCanvasa);
        this.ctx = this.canvas.getContext('2d');

        //wskazowki i jej dlugosc, grubosc i szerokosc
        this.wskGodzinowa = new Wskazowka(100, 8, 'black');
        this.wskMinutowa = new Wskazowka(150, 5, 'blue');
        this.wskSekundowa = new Wskazowka(180, 2, 'red');

        // zatrzymanie zegara
        this.czyPauza = false;
        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                this.czyPauza = !this.czyPauza;
            }
        });
    }

    // kreski na tarczy minutowe, godzinowe
    rysujTarcze() {
        this.ctx.font = "24px Arial";
        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "middle";
        this.ctx.fillStyle = "black";
        this.ctx.strokeStyle = "black";

        //60 kresek
    for (let i = 0; i < 60; i++) {
        this.ctx.save();
        let kat = (i * 6) * Math.PI / 180;
        this.ctx.rotate(kat);
        
        this.ctx.beginPath();
        
        //kreski godzinowe, minutowe i ich grubosc
        if (i % 5 === 0) {
            this.ctx.lineWidth = 3;
            this.ctx.moveTo(0, -190);
            this.ctx.lineTo(0, -220);
        } else {
            this.ctx.lineWidth = 2;
            this.ctx.moveTo(0, -210);
            this.ctx.lineTo(0, -220);
        }
        
        this.ctx.stroke();
        this.ctx.restore();
    }

    //godziny
    for (let i = 1; i <= 12; i++) {
            this.ctx.save();
            let kat = (i * 30) * Math.PI / 180;
            this.ctx.rotate(kat);
            this.ctx.translate(0, -180);
            this.ctx.rotate(-kat);
            this.ctx.fillText(i.toString(), 0, 0);
            this.ctx.restore();
        }
    }

    //odswiezanie zegara
    aktualizuj() {
        if (!this.czyPauza) {
            //pobranie aktualnej godz
            const teraz = new Date();
            const sekundy = teraz.getSeconds();
            const minuty = teraz.getMinutes();
            const godziny = teraz.getHours();

            //czyszczenie
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.save();
            this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);

            //rysowanie tarczy
            this.rysujTarcze();

            //przeliczenie kata
            const katS = (sekundy / 60) * 2 * Math.PI;
            const katM = ((minuty + sekundy / 60) / 60) * 2 * Math.PI;
            const katG = (((godziny % 12) + minuty / 60) / 12) * 2 * Math.PI;

            //rysowanie wskazowek
            this.wskGodzinowa.rysuj(this.ctx, katG);
            this.wskMinutowa.rysuj(this.ctx, katM);
            this.wskSekundowa.rysuj(this.ctx, katS);

            //kwiatek
            this.ctx.beginPath();
            this.ctx.lineWidth = 4;
            this.ctx.strokeStyle = 'green';
            this.ctx.moveTo(0, 100);
            this.ctx.lineTo(0, 160);
            this.ctx.stroke();

            this.ctx.beginPath();
            this.ctx.lineWidth = 4;
            this.ctx.strokeStyle = 'green';
            this.ctx.moveTo(17, 130);
            this.ctx.lineTo(0, 150);
            this.ctx.moveTo(-17, 130);
            this.ctx.lineTo(0, 150);
            this.ctx.stroke();

            this.ctx.fillStyle = 'red';

            this.ctx.beginPath();
            this.ctx.arc(0, 85, 12, 0, 2 * Math.PI);
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(0, 115, 12, 0, 2 * Math.PI);
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(-15, 100, 12, 0, 2 * Math.PI);
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(15, 100, 12, 0, 2 * Math.PI);
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(0, 100, 10, 0, 2 * Math.PI);
            this.ctx.fillStyle = 'yellow';
            this.ctx.fill();

            this.ctx.beginPath();
            this.ctx.arc(0, 0, 8, 0, 2 * Math.PI);
            this.ctx.fillStyle = 'black';
            this.ctx.fill();
            this.ctx.restore();
        }
        requestAnimationFrame(() => this.aktualizuj());
    }
}

const mojZegar = new Zegar('clockCanvas');
mojZegar.aktualizuj();