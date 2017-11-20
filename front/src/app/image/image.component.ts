import { Component, OnInit, OnDestroy } from '@angular/core';
import { Http, Response } from '@angular/http';
import { AuthenticationService } from '../authentication';
import { Router } from '@angular/router';
import { NavbarComponent } from '../navbar';
import { WebService } from '../webservices';
import { ImageData } from '../imagedata';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { CommentData } from '../commentdata';

@Component({
  selector: 'image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css'],
  providers: [WebService, AuthenticationService]
})
export class ImageComponent implements OnInit, OnDestroy {

  public imageInfo = new ImageData(-1, "", "", -1, "");
  public comments: [CommentData] = [];
  public commentForm: FormGroup;

  private curUser = localStorage.getItem('user');
  private img = null;

  constructor(
      private http: Http,
      private router: Router,
      private webservice: WebService,
      private route: ActivatedRoute
  ) {
      let group: any = {};
      group.image_id = new FormControl('', Validators.required);
      group.comment = new FormControl('', Validators.required);
      group.type = new FormControl('new-comment');
      this.commentForm = new FormGroup(group);
  }

  public ngOnInit() {
    this.webservice.isAuthenticated();

    this.sub = this.route.params.subscribe(params => {
        this.id = +params['id'];
    });
    this.getData();
  }

  public ngOnDestroy() {
    // Will clear when component is destroyed e.g. route is navigated away from.
    this.sub.unsubscribe();
    console.log('destroyed');
  }

  /**
   * Fetch the data from the python-flask backend
   */
  public getData() {
    this.webservice.getImage(this.id)
      .subscribe(
      (data) => this.handleImage(data),
      (err) => this.logError(err),
      () => console.log('got image')
      );

    this.webservice.getImageInfo(this.id)
      .subscribe(
      (data) => this.handleImageInfo(data),
      (err) => this.logError(err),
      () => console.log('got image info')
      );

    this.webservice.getComments(this.id)
      .subscribe(
      (data) => this.handleComments(data),
      (err) => this.logError(err),
      () => console.log('got comments')
      );
  }

  public refreshComments() {
      this.comments = [];
      this.webservice.getComments(this.id)
        .subscribe(
        (data) => this.handleComments(data),
        (err) => this.logError(err),
        () => console.log('got comments')
        );
  }

  public createComment() {
      let body = {
        image_id: this.imageInfo.id,
        comment: this.commentForm.controls['comment'].value
      };
      this.webservice.createComment(body)
        .subscribe((data) => {
          this.refreshComments();
          
          let group: any = {};
          group.image_id = new FormControl('', Validators.required);
          group.comment = new FormControl('', Validators.required);
          group.type = new FormControl('new-comment');
          this.commentForm = new FormGroup(group);
        },
        (error) => this.handleError(error)
        );
  }

  private handleImage(data: Response) {
    if (data.status === 200) {
      // console.log(data);
      // console.log(data._body);
      // this.img = data._body;
      this.img = b64EncodeUnicode(data._body)
    }
  }

  private handleImageInfo(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      this.imageInfo.name = receivedData['name'];
      this.imageInfo.caption = receivedData['caption'];
      this.imageInfo.owner = receivedData['owner'];
      this.imageInfo.id = receivedData['id'];
      this.imageInfo.timestamp = receivedData['timestamp'];
    }
  }

  private handleComments(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      for(var i=0; i < receivedData['comments'].length; i++) {
          this.comments.push(
              new CommentData(
                  receivedData['comments'][i]['author'],
                  receivedData['comments'][i]['comment'],
                  receivedData['comments'][i]['timestamp']
              )
          );
      }
    }
  }

  private logError(err: Response) {
    console.log('There was an error: ' + err.status);
    if (err.status === 0) {
      console.error('Seems server is down');
    }
    if (err.status === 401) {
      this.router.navigate(['/sessionexpired']);
    }
  }
}

function b64EncodeUnicode(str) {
    // first we use encodeURIComponent to get percent-encoded UTF-8,
    // then we convert the percent encodings into raw bytes which
    // can be fed into btoa.
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
        function toSolidBytes(match, p1) {
            return String.fromCharCode('0x' + p1);
    }));
}
