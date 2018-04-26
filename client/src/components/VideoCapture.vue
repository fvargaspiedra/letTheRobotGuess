<template>
  <div id="video-capture">
    <div class="video-container">
      <div><video ref="video" id="video" width="640" height="480" autoplay></video></div>
      <div class="crop-square"></div>
    </div>
    <div><button id="snap" @click="capture()">Snap Photo</button></div>
    <canvas ref="canvas" id="canvas" width="640" height="480"></canvas>

</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VideoCapture',
  data () {
    return {
      video: {},
      canvas: {}
    }
  },
  mounted () {
    this.video = this.$refs.video
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        this.video.src = window.URL.createObjectURL(stream)
        this.video.play()
      })
    }
  },
  methods: {
    capture () {
      this.canvas = this.$refs.canvas
      this.canvas.getContext('2d').drawImage(this.video, 0, 0, 640, 480)
      const image = this.canvas.toDataURL('image/png')
      console.log(image)
      axios.post('http://localhost:5000/classify', {
        image: image
      }).then((response) => {
        console.log(response)
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style lang="scss">
.video-container {
  position: relative;
}
.crop-square {
  position: absolute;
  width: 300px;
  height: 300px;
  left: calc(50% - 150px);
  top: calc(50% - 150px);
  z-index: 10;
  border: red solid 3px;
}
</style>
