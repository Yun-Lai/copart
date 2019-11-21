import {Component, Input, OnInit} from '@angular/core';
import {StartpageService} from "../../../utils/services/startpage.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-vehicle-finder',
  templateUrl: './vehicle-finder.component.html',
  styleUrls: ['./vehicle-finder.component.scss']
})
export class VehicleFinderComponent implements OnInit {

  @Input() status: string;
  @Input() vehicle_types: [];
  vehicle_all_makes = [];
  year_range = [];
  locations = [];
  models = ['All Models'];
  selected_vehicle_type = 'V';
  selected_year_range = [2008, 2019];
  selected_vehicle_makes = '0';
  selected_model = 'All Models';
  model_disabled = false;
  selected_location = 'All Locations';

  constructor(private _apiService: StartpageService, private router: Router) {
    this.selected_year_range[1] = new Date().getFullYear();
  }

  ngOnInit() {
    this.getYears();
    this.getLocations();
    this.getAllVehicleMakes();
  }
  getYears() {
    this._apiService.getYearRange().then( result => {
      this.year_range = result.year_range;
    }).catch( error => {
      console.log(error);
    });
  }
  getLocations() {
    this._apiService.getLocations().then( result => {
      this.locations = result.locations;
    }).catch( error => {
      console.log(error);
    });
  }
  getAllVehicleMakes() {
    this._apiService.getAllVehicleMakes(this.selected_vehicle_type).then( result => {
      this.vehicle_all_makes = result.vehicle_all_makes;
    }).catch( error => {
      console.log(error);
    });
  }
  selectType() {
    this.selected_vehicle_makes="0";
    this.selected_model = 'All Models';
    this.models = ['All Models'];
    this.getAllVehicleMakes();
  }
  selectMake() {
    this.models = ['All Models'];
    this.selected_model = 'All Models';
    this.model_disabled = true;
    if (this.selected_vehicle_makes === '0') {
      this.model_disabled = false;
      return;
    }
    this._apiService.getModels({"finder_type": this.selected_vehicle_type, "finder_make": this.selected_vehicle_makes}).then( result => {
      this.models = result.models;
      this.models.unshift('All Models');
      this.model_disabled = false;
    }).catch( error => {
      console.log(error);
    });
  }
  goToSearchPage() {
    let params = {};
    params['type'] = this.selected_vehicle_type;
    params['year'] = JSON.stringify(this.selected_year_range);
    params['status'] = JSON.stringify(["Sites", "Already Sold", "Featured Items", "Make"]);
    if (this.selected_vehicle_makes !== '0') {
      params['make'] = this.selected_vehicle_makes
    }
    if (this.selected_model !== 'All Models') {
      params['model'] = this.selected_model;
    }
    if (this.selected_location !== 'All Locations') {
      params['location'] = this.selected_location;
    }
    params['sort'] = JSON.stringify({"sort_by":"year","sort_type":"desc"});
    this.router.navigate(['/lots_by_search'], {queryParams: params});
  }
}
