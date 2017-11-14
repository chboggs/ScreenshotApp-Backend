import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Router } from '@angular/router';
import { jsonHeader } from '../utils';

var localstorage = window.localStorage;

@Injectable()
export class AuthenticationService {

  constructor(private http: Http, private router: Router) { }

  public isAuthenticated() {
    return localstorage.getItem('user');
  }

  public clearUserDataAndRedirect() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }

  /**
   * Sends a login request
   *
   */
  public login(body: object) {
    console.log(body)
    console.log(body['username'])
    localstorage.setItem('user', body['username'])
    return this.http.post('/api/login', body)
      .map(this.handleLogin)
      .catch(this.handleError);
  }

  public handleLogin(res: Response) {
    let body = res.json();
    console.log(localstorage.getItem('user'));
    if (res.status === 200) {
      
    }
  }

  /**
   * Logout method to send a logout request to the server and clear localStorage
   */
  public logout() {
    if (this.isAuthenticated()) {
      this.postResource('', '/api/logout')
        .subscribe((data) => this.handleLogout(data),
        (error) => {
          if (error.status === 401) {
            this.router.navigate(['/sessionexpired']);
          }
        },
        () => console.log('got data')
        );
    } else {
      this.clearUserDataAndRedirect();
    }
  }

  /**
   *
   * Post resource to send a post request to the server.
   * Extracts the current token from the local storage else redirects to
   * session expired modal.
   */
  public postResource(body: object, url: string) {
    // let token = localStorage.getItem('token');
    // let postHeader = new Headers({ Authorization: 'Bearer ' + token });
    // postHeader.append('Content-Type', 'application/json');
    // let options = new RequestOptions({ headers: postHeader });
    // return this.http.post(url, body, options);
    console.log(url)
    return this.http.post(url, body);
  }

  /**
   * Get resource to fetch data from server using an end point as `url`
   */
  public getResource(url: string) {
    // let token = localStorage.getItem('token');
    // let getHeader = new Headers({ Authorization: 'Bearer ' + token });
    // let options = new RequestOptions({ headers: getHeader });
    return this.http.get(url);
  }



  private handleError(error: any) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    this.loggedIn = false;
    this.loggedInUser = "";
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg); // log to console instead
    return Observable.throw(errMsg);
  }

  /**
   *
   * On logout, clear the local storage and redirect to login page
   */
  private handleLogout(data: Response) {
    if (data.status === 200) {
      localStorage.clear();
      this.router.navigate(['/login']);
    }
  }
}
