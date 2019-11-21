import { Component, OnInit } from '@angular/core';
import {StartpageService} from "../../../utils/services/startpage.service";

@Component({
  selector: 'app-new-arrival',
  templateUrl: './new-arrival.component.html',
  styleUrls: ['./new-arrival.component.scss']
})
export class NewArrivalComponent implements OnInit {

  arrivals = [];

  showExternal = false;
  constructor(private _apiService: StartpageService) { }

  ngOnInit() {
    this.getNewArrivals();
  }

  getNewArrivals() {
    this._apiService.getNewArrivals().then(result => {
      this.arrivals = result.arrivals;
    }).catch( error => {
      console.log(error);
    });
  }
  showExternalArrivals() {
    this.showExternal = true;
  }
  hideExternalArrivals() {
    this.showExternal = false;
  }

}
