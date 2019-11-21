import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {HostService} from "./host.service";

@Injectable({
  providedIn: 'root'
})
export class StartpageService {

  constructor(private http: HttpClient, private hostService: HostService) { }

  getVehicleTypes(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/vechiletyps/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getNewArrivals(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/newarrivals/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getFilterdItems(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/filtereditems/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getVehicleMakes(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/vehiclemakes/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getAllVehicleMakes(type): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/allvehiclemakes/', {params: {"type": type}}).subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getLocations(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/locations/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getYearRange(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/years/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getStatus(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/status/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getModels(filter): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/getmodels/', {params: filter}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
}
