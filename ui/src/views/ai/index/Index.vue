<template>
  <div class="box">
    <div class="start" @click="start"></div>
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'

  onMounted(() => {
    document.title = '青山司法AI智能解答'
  })

  const router = useRouter()

  const start = () => {
    router.push('/ai/chat')
  }
</script>

<style scoped>
  .box {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('../../../assets/images/index-bg.png') no-repeat top center / 100% 100%;
  }

  .start {
    position: absolute;
    bottom: 9.970014992503748vh;
    left: 28.8vw;
    width: 42.4vw;
    height: 4.497751124437781vh;
    cursor: pointer;
  }
</style>
