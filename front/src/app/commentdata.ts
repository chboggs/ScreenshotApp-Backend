export class CommentData {
  public author: string;
  public comment: string;
  public timestamp: string;

  constructor(
      private author: string,
      private comment: string,
      private timestamp: string
  ) {
      this.author = author;
      this.comment = comment;
      this.timestamp = timestamp;
  }
}
