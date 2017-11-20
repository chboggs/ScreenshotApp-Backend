export class ImageData {
  public name: string;
  public caption: string;
  public owner: string;
  public id: number;
  public timestamp: string;

  constructor(
      private name: string,
      private caption: string,
      private owner: string,
      private id: number,
      private timestamp: string
  ) {
      this.name = name;
      this.caption = caption;
      this.owner = owner;
      this.id = id;
      this.timestamp = timestamp;
  }
}
