import PostsList from "/components/PostsList.js";
export default {
    components: { PostsList },
    data() {
        return {
            meta: [],
            listStyle: {
                marginBottom: '8px'
            },
            spanStyle: {
                marginRight: '8px'
            }
        }
    },
    created() {
        this.meta = this.$postsMeta;
    },
    methods: {
        getDate(str) {
            let date = new Date(str);
            let month = date.getMonth() + 1;
            if (month < 10) {
                month = '0' + month
            }
            let day = date.getDate();
            if (day < 10) {
                day = '0' + day
            }
            return month + '-'
                + day + '-'
                + date.getFullYear();
        }
    },
    template: `
    <h1 style='border-bottom: 2px dashed var(--border-color);' class='title is-4' style='margin-bottom: 32px;'>ARCHIVE</h1>
    <posts-list :posts-data='meta'></posts-list>
    <!-- <ul>
        <li :style='listStyle' class='archive-post' v-for='item in meta'>
            <router-link class='title is-5' :to='"post/" + item.linkname'>[{{this.getDate(item.date)}}] - {{ item.title }}</router-link>
            <br/>
            <span :style='spanStyle' class='tag is-dark' v-for='tag in item.tags'>
            {{tag}}
            </span>
        </li>
    </ul> -->
    `
}