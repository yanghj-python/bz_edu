<template>
    <el-carousel height="720px" :interval="3000" arrow="always">
        <el-carousel-item v-for="(banner, key) in banner_list" :key="key">
            <a :href="banner.link"><img :src="banner.img" alt=""></a>
        </el-carousel-item>
    </el-carousel>

</template>

<script>
    export default {
        name: "Banner",
        // 获取轮播图的数据
        data(){
            return{
                banner_list:[], // 轮播图的数据
            }
        },
        methods:{
            get_all_banner(){
                this.$axios({
                    url:'http://127.0.0.1:9001/home/banner/',
                    method: "get",
                }).then(res=>{
                    // 当前请求的返回值可以通过res接受到
                    console.log(res.data);
                    this.banner_list = res.data;
                }).catch(error=>{
                    console.log(error);
                })
            },
        },
        // 在当前页面渲染之前将数据获取并赋值给 data
        created() {
            // 获取轮播图数据
            this.get_all_banner();
        }
    }
</script>

<style scoped>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 18px;
        opacity: 0.75;
        line-height: 300px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
</style>
