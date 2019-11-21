import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {HostService} from "./host.service";

@Injectable({
  providedIn: 'root'
})
export class DetailService {

  constructor(private http: HttpClient, private hostService: HostService) { }
  getSimilar(lot): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lot_similar_with_lot/' + lot.toString() + '/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getLotInfo(lot): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lot_info_with_lot/' + lot.toString() + '/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }
  getBidInfo(vin): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/bid_info_with_lot/' + vin + '/').subscribe(results => {
        resolve(results);
      }, error => {
        reject(error);
      });
    });
  }

  getWinningBids(lot): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/winning_bid_with_lot/' + lot + '/').subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      })
    })
  }

  getChartData(data): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/api_chart/', {params: data}).subscribe( result => {
        resolve(result)
      }, error => {
        reject(error)
      })
    })
  }

  getLot(id): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/api_get_lot_vin/' + id).subscribe( result => {
        resolve(result)
      }, error => {
        reject(error)
      })
    })
  }
}
