const app = Vue.createApp({
    data() {
        return {
            showMenu: false,
            showDropdown: false,
            isDesktop: window.innerWidth > 640,
        }
    },
    mounted() {
        window.addEventListener('resize', this.updateWidth);
        this.updateWidth();
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.updateWidth);
    },
    methods: {
        updateWidth() {
            this.isDesktop = window.innerWidth > 640;
            if (this.isDesktop) {
                this.showMenu = true;
            }
        }
    }


})

app.mount('#app')