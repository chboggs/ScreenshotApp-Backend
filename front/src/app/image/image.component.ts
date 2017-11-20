import { Component, OnInit, OnDestroy } from '@angular/core';
import { Http, Response } from '@angular/http';
import { AuthenticationService } from '../authentication';
import { Router } from '@angular/router';
import { NavbarComponent } from '../navbar';
import { WebService } from '../webservices';
import { ImageData } from '../imagedata';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css'],
  providers: [WebService, AuthenticationService]
})
export class ImageComponent implements OnInit, OnDestroy {

  public imageInfo = new ImageData(-1, "", "", -1, "");
  public comments = [];
  private curUser = localStorage.getItem('user');

  constructor(
      private http: Http,
      private router: Router,
      private webservice: WebService,
      private route: ActivatedRoute
  ) { }

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
    // this.webservice.getImage(this.id)
    //   .subscribe(
    //   (data) => this.handleImage(data),
    //   (err) => this.logError(err),
    //   () => console.log('got image')
    //   );

    this.webservice.getImageInfo(this.id)
      .subscribe(
      (data) => this.handleImageInfo(data),
      (err) => this.logError(err),
      () => console.log('got image info')
      );

    // this.webservice.getComments(this.id)
    //   .subscribe(
    //   (data) => this.handleComments(data),
    //   (err) => this.logError(err),
    //   () => console.log('got comments')
    //   );
  }

  private handleImage(data: Response) {
    // if (data.status === 200) {
    //   let receivedData = data.json();
    //   this.ownedImages = receivedData['images'];
    // } else {
    //   this.ownedImages = [];
    // }
    console.log('image');
    console.log(data._body);
  }

  private handleImageInfo(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      console.log("data");
      console.log(receivedData);
      console.log("caption");
      console.log(receivedData['caption']);
      this.imageInfo.name = receivedData['name'];
      this.imageInfo.caption = receivedData['caption'];
      this.imageInfo.owner = receivedData['owner'];
      this.imageInfo.id = receivedData['id'];
      this.imageInfo.timestamp = receivedData['timestamp'];
    }
    console.log(this.imageInfo);
  }

  private handleComments(data: Response) {
    // if (data.status === 200) {
    //   let receivedData = data.json();
    //   this.viewableImages = receivedData['images'];
    // } else {
    //   this.viewableImages = [];
    // }
    console.log('comments');
    console.log(data);
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
