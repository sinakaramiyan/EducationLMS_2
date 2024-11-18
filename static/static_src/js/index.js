import './../css/main.css';
import Alpine from 'alpinejs';
import './myhtmx';

class Index {
    constructor() {
        this.init();
    }

    init() {
        window.Alpine = Alpine
        Alpine.start();
    }
}

new Index()