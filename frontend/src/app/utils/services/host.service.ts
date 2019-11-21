import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HostService {
  rentCarUrl = 'localhost:8000';

  constructor(private http: HttpClient) {
    this.http.get(window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') +
      '/api/test/').toPromise().then( () => {
        this.rentCarUrl = window.location.hostname + (window.location.port ? ':' + window.location.port : '');
      }).catch( () => {
          this.rentCarUrl = window.location.hostname;
      });
  }

  init(http: HttpClient): Promise<any> {
    return http.get(window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') +
      '/api/test/').toPromise().then( () => {
        this.rentCarUrl = window.location.hostname + (window.location.port ? ':' + window.location.port : '');
      }).catch( () => {
          this.rentCarUrl = window.location.hostname;
      });
  }
  get ApplicationServerUrl(): string {
    return window.location.protocol + '//' + this.rentCarUrl + '/api';
  }
}
