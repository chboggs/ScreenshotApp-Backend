import { Component, OnInit, Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication';
import { Router } from '@angular/router';
import { Http, Response } from '@angular/http';

@Injectable()
export class WebService {
  constructor(private authService: AuthenticationService) { }

  public getOwnedImages() {
      return this.authService.getResource('/api/get-owned-images');
  }

  public getViewableImages() {
      return this.authService.getResource('/api/get-viewable-images');
  }

  public getImage(id: number) {
      return this.authService.getResource('/api/get-image?id=' + id);
  }

  public getImageInfo(id: number) {
      return this.authService.getResource('/api/get-image-info?id=' + id);
  }

  public getComments(id: number) {
      return this.authService.getResource('/api/get-comments?image_id=' + id);
  }

  /**
   * Send request for a new user
   *
   */
  public createUser(body: object) {
    return this.authService.postResource(body, '/api/new-user');
  }

  public createComment(body: object) {
      return this.authService.postResource(body, '/api/add-comment');
  }

  public addViewer(body: object) {
      return this.authService.postResource(body, '/api/add-viewer')
  }

  public isAuthenticated() {
    if (!this.authService.isAuthenticated()) {
      this.authService.clearUserDataAndRedirect();
    }
  }
}
