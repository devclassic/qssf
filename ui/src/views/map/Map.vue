<template>
  <baidu-map
    class="map"
    :zoom="12.9"
    :center="{ lng: 109.9, lat: 40.64 }"
    :dragging="true"
    :scroll-wheel-zoom="true"
    :double-click-zoom="true"
    :keyboard="true"
    :inertial-dragging="true"
    :continuous-zoom="true"
    :pinch-to-zoom="true"
    :auto-resize="true">
    <bm-label
      v-for="item of state.items"
      :content="item.title"
      :position="item.point"
      :labelStyle="{
        transform: 'translate(-50%, 30px)',
        borderRadius: '5px',
        padding: '5px',
        border: '2px solid #283f6b',
      }" />
    <bm-marker
      v-for="item of state.items"
      :position="item.point"
      :icon="state.pointIcon"
      animation="BMAP_ANIMATION_BOUNCE"
      @click="mapGaode(item)">
      <bm-info-window :show="item.show" @close="infoWindowClose(item)" @open="infoWindowOpen(item)">
        <div>{{ item.title }}</div>
        <div class="map-item" @click="mapGaode(item)">查看导航</div>
      </bm-info-window>
    </bm-marker>
    <bm-label
      v-show="state.showPos"
      content="我的位置"
      :position="state.pos"
      :labelStyle="{
        transform: 'translate(-50%, 3px)',
        borderRadius: '5px',
        padding: '5px',
        border: '2px solid red',
      }" />
    <bm-geolocation
      anchor="BMAP_ANCHOR_BOTTOM_RIGHT"
      :locationIcon="state.locationIcon"
      :showAddressBar="true"
      :autoLocation="true"
      @locationSuccess="locationSuccess"
      @locationError="locationError" />
  </baidu-map>
</template>

<script setup>
  import { onMounted, reactive } from 'vue'
  import { ElMessageBox } from 'element-plus'
  import point from '../../assets/images/point.png'
  import pos from '../../assets/images/pos.png'
  console.log(point)

  const state = reactive({
    items: [
      { title: '青山区司法局福强路司法所', point: { lat: 40.67719, lng: 109.86651 }, show: false },
      { title: '青山区司法局科学路司法所', point: { lat: 40.67218, lng: 109.85491 }, show: false },
      { title: '青山区司法局青福镇司法所', point: { lat: 40.64957, lng: 109.91699 }, show: false },
      { title: '青山区司法局青山路司法所', point: { lat: 40.66712, lng: 109.89434 }, show: false },
      { title: '青山区司法局万青路司法所', point: { lat: 40.64793, lng: 109.86786 }, show: false },
      { title: '青山区司法局乌素图司法所', point: { lat: 40.65692, lng: 109.95531 }, show: false },
      { title: '青山区司法局先锋道司法所', point: { lat: 40.67303, lng: 109.87981 }, show: false },
      { title: '青山区司法局兴盛镇司法所', point: { lat: 40.67229, lng: 109.92981 }, show: false },
      { title: '青山区司法局幸福路司法所', point: { lat: 40.66626, lng: 109.87191 }, show: false },
      { title: '青山区司法局自由路司法所', point: { lat: 40.66407, lng: 109.89297 }, show: false },
    ],
    pointIcon: {
      url: point,
      size: { width: 50, height: 50 },
      opts: { imageSize: { width: 50, height: 50 } },
    },
    locationIcon: {
      url: pos,
      size: { width: 40, height: 40 },
      opts: { imageSize: { width: 40, height: 40 } },
    },
    pos: {},
    showPos: false,
  })

  onMounted(() => {
    document.title = '青山司法局司法所分布'
    ElMessageBox.alert('点击右下角可定位到您的位置', '温馨提示')
  })

  const infoWindowOpen = item => {
    item.show = true
  }

  const infoWindowClose = item => {
    item.show = false
  }

  const mapGaode = item => {
    location.href = `https://uri.amap.com/marker?name=${item.title}&position=${item.point.lng},${item.point.lat}`
  }

  const locationSuccess = e => {
    state.pos = e.point
    state.showPos = true
  }

  const locationError = e => {
    state.showPos = false
    alert(e.message)
  }
</script>

<style scoped>
  .map {
    width: 100vw;
    height: 100vh;
  }

  .map-item {
    margin-top: 10px;
    font-size: 14px;
    color: blue;
    cursor: pointer;
  }
</style>
