import { Component, OnInit, OnDestroy } from '@angular/core';
import { Http, Response } from '@angular/http';
import { AuthenticationService } from '../authentication';
import { Router } from '@angular/router';
import { NavbarComponent } from '../navbar';
import { WebService } from '../webservices';
import { Image } from '../image';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [WebService, AuthenticationService]
})
export class HomeComponent implements OnInit, OnDestroy {

  public ownedImages = [];
  public viewableImages = [];
  private curUser = localStorage.getItem('user')
  constructor(private http: Http, private router: Router, private webservice: WebService) { }

  public ngOnInit() {
    this.webservice.isAuthenticated();
    this.getData();
  }

  public ngOnDestroy() {
    // Will clear when component is destroyed e.g. route is navigated away from.
    console.log('destroyed');
  }

  public clear() {
    this.ownedImages = [];
    this.viewableImages = [];
  }

  /**
   * Fetch the data from the python-flask backend
   */
  public getData() {
    this.webservice.getOwnedImages()
      .subscribe(
      (data) => this.handleOwnedImages(data),
      (err) => this.logError(err),
      () => console.log('got owned images')
      );

    this.webservice.getViewableImages()
      .subscribe(
      (data) => this.handleViewableImages(data),
      (err) => this.logError(err),
      () => console.log('got viewable images')
      );
  }

  private handleOwnedImages(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      this.ownedImages = receivedData['images'];
    }
    console.log(data.json());
  }
  private handleViewableImages(data: Response) {
    if (data.status === 200) {
      let receivedData = data.json();
      this.viewableImages = receivedData['images'];
    }
    console.log(data.json());
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
