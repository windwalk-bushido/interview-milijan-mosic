class Todo {
  uuid: any;
  body: string;
  done: boolean;

  constructor(uuid: any, body: string, done: boolean) {
    this.uuid = uuid;
    this.body = body;
    this.done = done;
  }
}

export default Todo;
