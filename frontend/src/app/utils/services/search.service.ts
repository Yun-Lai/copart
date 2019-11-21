import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {HostService} from "./host.service";


@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient, private hostService: HostService) { }

  getSearchList(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListFeatures(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_features/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListCount(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_count_searched/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListMake(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_make/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListModel(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_model/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }

  getSearchListYearLocation(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_year_location/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListTransmissionCylinder(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_transmission/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListFuelEngine(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_fuel/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }
  getSearchListVehicleDamage(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_by_summary_vehicle_damage/', {params: params}).subscribe( result => {
        resolve(result);
      }, error => {
        reject(error);
      });
    });
  }

  getPagnagedData(params): Promise<any> {
    return new Promise( (resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/lots_paged_by_search/', {params: params}).subscribe( result => {
        resolve(result)
      }, error => {
        reject(error)
      })
    })
  }

  getSearchKey(params): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(this.hostService.ApplicationServerUrl + '/api_filter_key/', {params: params}).subscribe( result => {
        resolve(result)
      }, error => {
        reject(error)
      })
    })
  }
}
