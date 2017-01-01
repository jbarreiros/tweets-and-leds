class Socket {
  constructor(url) {
    this.callbacks = {};
    this.ws = new WebSocket(url);
    this.ws.onopen = this.onOpen;
    this.ws.onerror = this.onError;
    this.ws.onmessage = this.onMessage;
  }

  onOpen() {
    console.info('Websocket opened!');
  }

  onError(err) {
    console.error('Websocket error: ', err);
  }

  onMessage = (e) => {
    let data = {};

    try {
      data = JSON.parse(e.data);
      console.info('Websocket message received: ', data);
    } catch(e) {
      console.error('Unable to parse message: ', e.message);
      return;
    }

    if (!data.hasOwnProperty('event')) {
      console.warn('Websocket message is missing event name');
      return;
    }

    if (!this.callbacks.hasOwnProperty(data.event)) {
      console.warn(`No callacks registered for websocket message event: "${data.event}"`);
      return;
    }

    let payload = Object.assign({}, data);
    delete payload.event;

    this.callbacks[data.event].forEach((callback) => {
      callback(payload);
    })
  }

  register(event, callback) {
    if (typeof callback !== 'function') {
      throw new TypeError('Provided callback is not a function');
    }

    if (!this.callbacks.hasOwnProperty(event)) {
      this.callbacks[event] = [];
    }

    this.callbacks[event].push(callback);
  }

  sendMessage(event, data) {
    try {
      let payload = Object.assign({event}, data);
      console.info('Sending websocket message: ', payload);
      this.ws.send(JSON.stringify(payload));
    } catch (e) {
      throw TypeError('The data parameter must be an object: ' + e.message);
    }
  }
}

export default Socket
