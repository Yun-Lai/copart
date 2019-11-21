import { Component, OnInit } from '@angular/core';
import {DetailService} from "../../../utils/services/detail.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  searchKey="";

  constructor(private detailService: DetailService, private router: Router) { }

  ngOnInit() {
  }

  goToLot(){
    this.detailService.getLot(this.searchKey).then(result => {
      if (result.status) {
        this.router.navigate(['/lot/' + result.lot]);
      }
    })
  }

}
