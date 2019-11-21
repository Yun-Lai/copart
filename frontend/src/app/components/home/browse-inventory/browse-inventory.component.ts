import {Component, Input, OnInit} from '@angular/core';
import {StartpageService} from "../../../utils/services/startpage.service";
import {Router} from "@angular/router";
import {DataShareService} from "../../../utils/services/data-share.service";

import { HttpParameterCodec } from "@angular/common/http";

@Component({
  selector: 'app-browse-inventory',
  templateUrl: './browse-inventory.component.html',
  styleUrls: ['./browse-inventory.component.scss']
})
export class BrowseInventoryComponent implements OnInit {

  @Input() status: string;
  @Input() vehicle_types: [];
  vehicle_makes = [];
  featured_filters = [];
  constructor(private _apiService: StartpageService, private router: Router, public dataShare: DataShareService) { }

  ngOnInit() {
    this.getFeaturedFilters();
    this.getVehicleMakes();
  }
  getFeaturedFilters() {
    this._apiService.getFilterdItems().then( result => {
      this.featured_filters = result.featured_filters;
    }).catch(error => {
      console.log(error);
    });
  }
  getVehicleMakes() {
    this._apiService.getVehicleMakes().then( result => {
      this.vehicle_makes = result.vehicle_makes;
    }).catch( error => {
      console.log(error)
    });
  }
  goSearch(params) {
    params['status'] = JSON.stringify(["Sites", "Already Sold", "Featured Items", "Make"]);
    params['sort'] = JSON.stringify({"sort_by":"year","sort_type":"desc"});
    this.router.navigate(['/lots_by_search'], {queryParams: params});
  }
  showTabs(id: string) {
    let item1 = document.getElementById('featured');
    let item2 = document.getElementById('vehicleType');
    let item3 = document.getElementById('makes');
    item1.classList.remove('show');
    item2.classList.remove('show');
    item3.classList.remove('show');
    let showItem = document.getElementById(id);
    showItem.classList.add('show');
    let aItem1 = document.getElementById('a_featured');
    let aItem2 = document.getElementById('a_vehicleType');
    let aItem3 = document.getElementById('a_makes');
    aItem1.classList.remove('active');
    aItem2.classList.remove('active');
    aItem3.classList.remove('active');

    let showAItem = document.getElementById('a_' + id);
    showAItem.classList.add('active');
  }
}
