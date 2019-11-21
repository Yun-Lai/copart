import { Component, OnInit } from '@angular/core';
import {StartpageService} from "../../utils/services/startpage.service";
import { Title } from '@angular/platform-browser';
import {LoaderService} from "../../utils/services/loader.service";

@Component({
  selector: 'app-start',
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss']
})
export class StartComponent implements OnInit {

  status = '';
  vehicle_types = [];

  constructor(public _apiService: StartpageService, private title: Title, public loader: LoaderService) { }
  ngOnInit() {
    this.title.setTitle("Home");
    this.getVehicleTypes();
    this.getStatus();
  }
  getVehicleTypes() {
    this._apiService.getVehicleTypes().then(result => {
      this.vehicle_types = result.vehicle_types;
    }).catch(error => {
      console.log(error);
    });
  }
  getStatus() {
    this._apiService.getStatus().then(result => {
      this.status = result.status;
    }).catch(error => {
      console.log(error);
    });
  }
}
