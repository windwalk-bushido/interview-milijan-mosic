class Todo {
  index: number;
  body: string;
  done: boolean;

  constructor(index: number, body: string, done: boolean) {
    this.index = index;
    this.body = body;
    this.done = done;
  }
}

export default Todo;
