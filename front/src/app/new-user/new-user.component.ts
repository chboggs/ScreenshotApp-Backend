import { Component, Injectable, ViewChild, OnInit } from '@angular/core';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { AuthenticationService } from '../authentication/authentication.service';
import { WebService } from '../webservices/webservices.services';
import { UserComponent } from '../utils/user';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Rx';

@Component({
  selector: `new-user`,
  templateUrl: './new-user.component.html',
  styleUrls: ['./new-user.component.css'],
  providers: [AuthenticationService]
})
export class NewUserFormComponent implements OnInit {

  public inputLogo = 'assets/img/logo.png';
  public model: UserComponent = new UserComponent(1, '', '');
  public newUserText: string = 'Enter information';
  public color: string = 'black';
  public myForm: FormGroup;

  constructor(private _service: AuthenticationService, private _webservice: WebService, 
    private router: Router) {
    let group: any = {};
    group.username = new FormControl('', Validators.required);
    group.password = new FormControl('', Validators.required);
    group.firstName = new FormControl('', Validators.required);
    group.lastName = new FormControl('', Validators.required);
    group.email = new FormControl('', Validators.required);
    group.type = new FormControl('new-user');
    this.myForm = new FormGroup(group);
  }

  public ngOnInit() {
    console.log('Inside the new-user page');

    if (this._service.isAuthenticated()) {
      console.log('Already logged in as a user');
      this.router.navigate(['/home']);
    }
  }

  public createUser() {
    let body = {
      username: this.myForm.controls['username'].value,
      password: this.myForm.controls['password'].value,
      first_name: this.myForm.controls['firstName'].value,
      last_name: this.myForm.controls['lastName'].value,
      email: this.myForm.controls['email'].value,
    };
    this._webservice.createUser(body)
      .subscribe((data) => {
        this.router.navigate(['/login']);
      },
      (error) => this.handleError(error)
      );
  }
  private handleError(error: any) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg); // log to console instead
    this.color = 'red';
    this.logintext = errMsg;
    return Observable.throw(errMsg);
  }
}
