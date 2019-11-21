import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {

  lot: number;
  constructor(public route: ActivatedRoute) {

    // this.lot = parseInt(this.route.snapshot.params['lot']);
  }

  ngOnInit() {
  }
}
