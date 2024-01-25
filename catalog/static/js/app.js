const app = Vue.createApp({
        data() {
            return {
                showMenu: false,
                showDropdown: false,
                showDropdownAccount: false,
                showSummary: false,
                showSummaryAuthorDetail: false,
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
            }

        }


    }
)


app.mount('#app')

