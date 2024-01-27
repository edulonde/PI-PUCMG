const app = Vue.createApp({
        data() {
            return {
                showMenu: false,
                showDropdown: false,
                showDropdownAccount: false,
                showSummary: false,
                showSummaryAuthorDetail: false,
                showBorrowed: false,
                showFavorites: false,
                showHistory: false,
                statusClasses: {
                    'd': 'bg-green-500',
                    'r': 'bg-yellow-500',
                    'e': 'bg-orange-500',
                    'm': 'bg-red-500',
                },



            }
        },
        methods: {
            toggleSummary() {
                this.showSummary = !this.showSummary
            },
            toggleSummaryAuthorDetail() {
                this.showSummaryAuthorDetail = !this.showSummaryAuthorDetail
            },
            toggleDropdownAccount() {
                this.showDropdownAccount = !this.showDropdownAccount
            },
            toggleBorrowed() {
                this.showBorrowed = !this.showBorrowed;
            },
            toggleFavorites() {
                this.showFavorites = !this.showFavorites;
            },
            toggleHistory() {
                this.showHistory = !this.showHistory;
            },


        }


    }
)


app.mount('#app')

