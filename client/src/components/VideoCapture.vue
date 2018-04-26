<template>
  <div id="video-capture">
    <div class="controls">
      <button @click="play()" v-if="state !== 'gameStarted'">Let's Play!</button>
      <button id="snap" @click="capture()" v-if="state === 'gameStarted'">Take Picture</button>
    </div>
    <div class="game">
      <div class="video-container">
        <div><video ref="video" id="video" width="640" height="480" autoplay></video></div>
        <div class="crop-square"></div>
      </div>
      <div class="messages">
        <p v-if="selectedCategory" class="messages__draw">Draw: {{ selectedCategory }}</p>
        <p v-if="guessed" class="messages__guess">Robo-guess: {{ guessed }}</p>
        <p v-if="accuracy" class="messages__accuracy">Accuracy: {{ accuracy }}</p>
      </div>
    </div>
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
      canvas: {},
      categories: [],
      state: 'notStarted',
      gameStarted: false,
      gameCompleted: false,
      gameWon: false,
      guessed: '',
      selectedCategory: '',
      accuracy: ''

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
      this.guessed = ''
      this.accuracy = ''
      this.canvas = this.$refs.canvas
      this.canvas.getContext('2d').drawImage(this.video, 0, 0, 640, 480)
      const image = this.canvas.toDataURL('image/png')
      axios.post('http://localhost:5000/classify', {
        image: image
      }).then((response) => {
        this.guessed = response.data.guess
        this.accuracy = response.data.accuracy
        if (response.data.guess === this.selectedCategory) {
          this.state = 'gameCompleted'
        }
      }).catch((error) => {
        console.log(error)
      })
    },
    play() {
      axios.get('http://localhost:5000/getLabels').then((response) => {
        console.log(response)
        this.categories = response.data
        this.state = 'gameStarted'
        this.selectedCategory = this.categories[Math.floor(Math.random() * this.categories.length)]
        console.log(this.selectedCategory)
      });
    }
  }
}
</script>

<style lang="scss">
.controls {
  margin-bottom: 50px;
  text-align: center;
}
button {
  padding: 10px 30px;
  color: #fff;
  background-color: #4DA1CD;
  border-radius: 3px;
  border: none;
  font-size: 20px;
  font-weight: bold;
  &:hover, &:active {
    background-color: darken(#4DA1CD, 10%);
  }
}
.game {
  display: flex;
}
.video-container {
  position: relative;
  flex: 0 0 640px;
}
.messages {
  flex: 1 1 auto;
  margin-left: 30px;
  font-size: 24px;
  p {
    margin-top: 0;
  }
}
.messages__guess {
  margin-bottom: 10px;
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
#canvas {
  display: none;
}
</style>
