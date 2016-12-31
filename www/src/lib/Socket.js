class Socket {
  constructor(url) {
    this.callbacks = [];
    this.ws = new WebSocket(url);
    this.ws.onopen = this.onOpen;
    this.ws.onerror = this.onError;
    this.ws.onmessage = this.onMessage;
  }

  onOpen() {
    console.log('Websocket opened!');
  }

  onError(err) {
    console.log('Websocket error: ', err);
  }

  onMessage = (e) => {
    if (typeof e === 'undefined') {
      return;
    }

    const data = JSON.parse(e.data);
    console.log('Websocket message received: ', data);
    this.callbacks.forEach((callback) => {
      callback(data);
    })
  }

  register(callback) {
    if (typeof callback === 'function') {
      this.callbacks.push(callback);
    }
  }

  sendMessage(data) {
    console.log('Sending websocket message: ', data);
    this.ws.send(JSON.stringify(data));
  }
}

export default Socket
