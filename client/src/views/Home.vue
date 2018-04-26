<template>
  <div class="home">
    <video-capture></video-capture>
  </div>
</template>

<script>
// @ is an alias to /src
import VideoCapture from '@/components/VideoCapture.vue'

export default {
  name: 'home',
  components: {
    VideoCapture
  }
}
</script>
