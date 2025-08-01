<template>
  <div class="box">
    <div class="back" @click="back"></div>
    <div ref="content" class="content">
      <div class="wrap">
        <div class="chat"></div>
        <div class="banner"></div>
        <div class="datetime">{{ state.datetime }}</div>
        <div
          v-for="message of state.messages"
          class="chat-item"
          :class="message.type"
          :key="message.id">
          <div v-html="message.text" class="chat-box"></div>
        </div>
      </div>
    </div>
    <div class="input-box">
      <input v-model="state.input" @keyup="inputKeyup" class="input" />
      <div class="send" @click="send"></div>
    </div>
  </div>
</template>

<script setup>
  import { reactive, useTemplateRef, nextTick, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { v4 as uuidv4 } from 'uuid'
  import { useWindowSize } from '@vueuse/core'
  import { format } from 'date-fns'
  import axios from 'axios'
  import { fetchEventSource } from '@microsoft/fetch-event-source'
  import markdownit from 'markdown-it'

  const user = uuidv4()
  const md = markdownit()

  const state = reactive({
    datetime: format(new Date(), 'yyyy年MM月dd日'),
    input: '',
    messages: [
      {
        id: uuidv4(),
        type: 'left',
        text: '嗨！我是贴身法律顾问小AI',
      },
    ],
  })

  const router = useRouter()
  const contentRef = useTemplateRef('content')
  const { _, height } = useWindowSize()

  watch(height, () => {
    contentRef.value.scrollTo({
      top: contentRef.value.scrollHeight,
    })
  })

  const back = () => {
    router.back()
  }

  const setMessage = (id, message) => {
    const index = state.messages.findIndex(item => item.id === id)
    if (index !== -1) {
      state.messages[index].text = message
    }
  }

  const processMessage = async question => {
    const message = {
      id: uuidv4(),
      type: 'left',
      text: '正在思考中...',
    }
    state.messages.push(message)
    await nextTick()
    contentRef.value.scrollTo({
      top: contentRef.value.scrollHeight,
      behavior: 'smooth',
    })
    const baseUrl = import.meta.env.VITE_API_BASE_URL ?? ''
    const url = baseUrl + '/api/chat'

    const ctrl = new AbortController() // 随时可中断
    let answer = '' // 累加显示

    await fetchEventSource(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user, query: question }),
      signal: ctrl.signal,

      // 连接成功
      async onopen(res) {
        if (res.ok && res.headers.get('content-type')?.includes('text/event-stream')) {
          console.log('✅ SSE opened')
        } else {
          throw new Error(await res.text())
        }
      },

      // 每收到一条 SSE 推送
      async onmessage(ev) {
        if (ev.data === '[DONE]') return // Dify 结束标志
        try {
          const chunk = JSON.parse(ev.data)
          answer += chunk.answer || ''
          setMessage(message.id, answer ? md.render(answer) : '正在思考中...')
          await nextTick()
          contentRef.value.scrollTo({
            top: contentRef.value.scrollHeight,
            behavior: 'smooth',
          })
        } catch (e) {
          /* 非 JSON 片段直接忽略 */
        }
      },

      onerror(err) {
        console.error(err)
        ctrl.abort() // 出错时关闭连接
      },

      onclose() {
        console.log('🔚 SSE closed')
      },
    })
  }

  const send = () => {
    if (state.input.trim()) {
      state.messages.push({
        id: uuidv4(),
        type: 'right',
        text: state.input,
      })
      processMessage(state.input)
      state.input = ''
    }
  }

  const inputKeyup = event => {
    if (event.key === 'Enter') {
      send()
    }
  }
</script>

<style scoped>
  .box {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('../../../assets/images/chat-bg.png') no-repeat center center / 100% 100%;
  }

  .back {
    position: absolute;
    top: 14.66666666666667vw;
    left: 6.933333333333333vw;
    width: 6.133333333333333vw;
    height: 4vw;
    background: url('../../../assets/images/chat-back.png') no-repeat center center / 100% 100%;
    z-index: 1000;
  }

  .content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 30.66666666666667vw;
    overflow-y: auto;
  }

  .wrap {
    width: 87.33333333333333vw;
    margin: 0 auto;
  }

  .chat {
    width: 24vw;
    height: 9.333333333333333vw;
    background: url('../../../assets/images/chat-chat.png') no-repeat center center / 100% 100%;
    margin: 12.66666666666667vw auto 0;
  }

  .banner {
    width: 100%;
    height: 65.33333333333333vw;
    background: url('../../../assets/images/chat-banner.png') no-repeat center center / 100% 100%;
    margin-top: 1.333333333333333vw;
  }

  .datetime {
    text-align: center;
    color: #868686;
    margin: 6.666666666666667vw 0 6.666666666666667vw;
    font-size: 4vw;
  }

  .chat-item {
    margin-bottom: 5.333333333333334vw;
  }

  .chat-item::after {
    content: '';
    display: table;
    clear: both;
  }

  .chat-box {
    max-width: 67.06666666666667vw;
    padding: 3.333333333333333vw 6.666666666666667vw;
    font-size: 4vw;
    color: #868686;
    box-shadow: 0px 2px 2px 2px rgba(39, 115, 190, 0.18);
    word-break: break-all;
  }

  .chat-item.left .chat-box {
    float: left;
    border-radius: 0 20px 20px 20px;
    background: #ddedff;
  }

  .chat-item.right .chat-box {
    float: right;
    border-radius: 20px 0 20px 20px;
    background: #ffffff;
  }

  .chat-item.right .chat-box .header {
    background: url('../../../assets/images/chat-box-header-right.png') no-repeat center center /
      100% 100%;
  }

  .chat-item.right .chat-box .text {
    background: url('../../../assets/images/chat-box-bg-right.png') no-repeat center center / 100%
      100%;
  }

  .chat-item.right .chat-box .footer {
    background: url('../../../assets/images/chat-box-footer-right.png') no-repeat center center /
      100% 100%;
  }

  .input-box {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: 10.66666666666667vw;
    width: 80vw;
    height: 12vw;
    background: url('../../../assets/images/chat-input.png') no-repeat center center / 100% 100%;
  }

  .input {
    width: 55vw;
    height: 6.666666666666667vw;
    line-height: 6.666666666666667vw;
    font-size: 4vw;
    color: #868686;
    background: transparent;
    border: none;
    outline: none;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-52.5%, -60%);
  }

  .send {
    position: absolute;
    top: 2vw;
    right: 4.666666666666667vw;
    width: 6.666666666666667vw;
    height: 6.666666666666667vw;
    cursor: pointer;
  }
</style>
