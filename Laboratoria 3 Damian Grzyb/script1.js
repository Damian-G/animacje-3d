class Particle {
    constructor(x, y, vx, vy, hue) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.hue = hue;
        this.alpha = 1.0;
        this.active = true;
        this.decay = Math.random() * 0.005 + 0.004; 
    }

    //aktualizacja fizyki czasteczki
    update(gravity, canvasHeight) {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += gravity;
        this.vx *= 0.96;
        this.vy *= 0.94;
        this.alpha -= this.decay;

        if (this.alpha <= 0) this.active = false;

        //odbijanie czasteczek od ziemi
        if (this.y >= canvasHeight) {
            this.y = canvasHeight;
            this.vy *= -0.8;
            this.vx *= 0.9;
        }
    }

    draw(ctx) {
        ctx.fillStyle = `hsla(${this.hue}, 100%, 50%, ${this.alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 1.2, 0, Math.PI * 2);
        ctx.fill();
    }
}

class Firework {
    constructor(startX, startY, targetX, targetY) {
        this.x = startX;
        this.y = startY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.active = true;
        this.exploded = false;
        this.hue = Math.random() * 360;
        this.speed = 8; 
        
        //wektor ruchu
        const dx = targetX - startX;
        const dy = targetY - startY;
        const dist = Math.hypot(dx, dy);
        
        this.vx = (dx / dist) * this.speed;
        this.vy = (dy / dist) * this.speed;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        //czy rakieta dotarla do celu
        if (Math.hypot(this.targetX - this.x, this.targetY - this.y) < 5) {
            this.exploded = true;
            this.active = false;
        }
    }

    //tablica czasteczek
    explode(n) {
        const particles = [];
        for (let i = 0; i < n; i++) {
            const angle = Math.random() * Math.PI * 2;
            const force = Math.random() * 5 + 1; 
            const vx = Math.cos(angle) * force;
            const vy = Math.sin(angle) * force;
            particles.push(new Particle(this.x, this.y, vx, vy, this.hue));
        }
        return particles;
    }

    draw(ctx) {
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fill();
    }
}

class FireworkShow {
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gravSlider = document.getElementById('gravSlider');
        this.countSlider = document.getElementById('countSlider');
        this.particles = [];
        this.rockets = [];
        
        this.flashAlpha = 0;

        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.canvas.addEventListener('click', (e) => {
            this.spawnRocket(e.clientX, e.clientY);
        });

        this.loop();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    //nowa rakieta z dolu ekranu
    spawnRocket(tx, ty) {
        const startX = this.canvas.width / 2;
        const startY = this.canvas.height;
        this.rockets.push(new Firework(startX, startY, tx, ty));
    }

    loop() {
        //efekt smug
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        //obsluga blysku tla
        if (this.flashAlpha > 0) {
        this.ctx.fillStyle = `rgba(255, 255, 255, ${this.flashAlpha})`;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.flashAlpha -= 0.02;
        }
        
        const gravity = parseFloat(this.gravSlider.value);
        const pCount = parseInt(this.countSlider.value);
        document.getElementById('gravVal').innerText = gravity;
        document.getElementById('countVal').innerText = pCount;

        //automatyczne fajerwerki
        if (Math.random() < 0.01) {
            const rx = Math.random() * this.canvas.width;
            const ry = Math.random() * (this.canvas.height * 0.6);
            this.spawnRocket(rx, ry);
        }

        //aktualizacaj i rysowanie rakiet
        this.rockets.forEach(r => {
            r.update();
            r.draw(this.ctx);
            if (r.exploded) {
                this.particles.push(...r.explode(pCount));
                this.flashAlpha = 0.05;
            }
        });

        //rysowanie czasteczek z trybem mieszania kolorow
        this.ctx.globalCompositeOperation = 'lighter';
        this.particles.forEach(p => {
            p.update(gravity, this.canvas.height);
            p.draw(this.ctx);
        });
        this.ctx.globalCompositeOperation = 'source-over';

        //usuwanie nieaktywnych obiektow
        this.rockets = this.rockets.filter(r => r.active);
        this.particles = this.particles.filter(p => p.active);

        requestAnimationFrame(() => this.loop());
    }
}

const show = new FireworkShow();