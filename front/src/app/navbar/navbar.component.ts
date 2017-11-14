import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../authentication';

@Component({
  selector: 'navbar',
  templateUrl: 'navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  public inputLogo = 'assets/img/logo.png';
  private curUser = "Not Logged In"
  constructor(private authService: AuthenticationService) { 
  	var userInfo = authService.getUser();
  	this.curUser = userInfo['user'];
  }

  public logout() {
    this.authService.logout();
  }
}
