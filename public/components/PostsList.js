import PostThumb from "./PostThumb.js";

export default {
    components: {PostThumb},
    props: ['postsData'],
    data() {
        return {
            posts: [],
            listStyle: {
                marginBottom: '8px'
            },
            spanStyle: {
                marginRight: '2px'
            }
        }
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
        <div class="columns is-multiline">
            <div :class="'column ' + ((index > 2 || index < 1) ? 'is-full' : '')" v-for="(post, index) in postsData">
                <PostThumb :postMeta="post" :isFirst="index == 0"/>
            </div>
        </div>
        <!-- <ul>
            <li :style='listStyle' class='archive-post' v-for='item in postsData'>
                <router-link style="padding-bottom: 16px;" :to='"/post/" + item.linkname'>
                <h2 class='title is-4'>[{{ item.category }}] - {{ item.title }}</h2>
                <p class='subtitle is-6'><i class="fa-regular fa-calendar"></i> {{ this.getDate(item.date) }}</p>
                </router-link>
                <br/>
                <div class='tags'>
                    <span :style='spanStyle' class='tag is-dark' v-for='tag in item.tags'>
                    {{tag}}
                    </span>
                </div>
            </li>
        </ul> -->
    `
}