import {Component, Input, OnInit, AfterViewInit, ViewChild} from '@angular/core';
import {DetailService} from "../../../utils/services/detail.service";
import {ActivatedRoute} from "@angular/router";
import {GetImagePipe} from "../../../utils/pipe/get-image.pipe";
import {Router} from "@angular/router";

import { ModelService } from "../../../utils/services/model.service";
import {LoaderService} from "../../../utils/services/loader.service";

@Component({
  selector: 'app-lot-detail',
  templateUrl: './lot-detail.component.html',
  styleUrls: ['./lot-detail.component.scss']
})
export class LotDetailComponent implements OnInit {

  bodyText: string;

  lot: number;
  lotDetail: any;
  selected_image = 0;
  winningBidDetails: any[] = [];
  sold: boolean = false;
  showBids = false;
  selected = -1;
  winningBids: any[] = [];
  noAuction = false;
  relisted = false;
  showFullHistory = false;
  min = 0;
  max = 0;
  avg = 0;
  url = './assets/chart/index.html';
  sold_status = false;
  show_fullReports = false;
  soldBidDetails: any[] = [];
  foregoingBidDetail: any[] = [];
  showDetails = false;
  historyLength = 0;
  loading = true;
  respond = false;

  constructor(private _api: DetailService, private route: ActivatedRoute,
              private pipe: GetImagePipe, private modalService: ModelService, private router: Router) {
    this.route.url.subscribe( url => {
      this.show_fullReports = false;
      this.lot = parseInt(this.route.snapshot.params['lot']);
      this.historyLength = 0;
      this.loading = true;
      this.url = './assets/chart/index.html';
      this.getInfo();
    });

  }

  ngOnInit() {

  }
  getChartData(data) {
    this._api.getChartData(data).then( result => {
      this.min = result['data']['sold_price__min'];
      this.max = result['data']['sold_price__max'];
      this.avg = result['data']['sold_price__avg'];
      let chart_lots = result['lots'];
      this.respond = true;
      setTimeout(() => {
        if (chart_lots.length < 3) {
          this.sold_status = false;
        } else {
          this.sold_status = true;
        }
      }, 100);
    }).catch(error => {
      console.log(error);
      this.router.navigate(['/'])
      this.respond = true;
    })
  }

  setShowFullHistory() {
    this.showFullHistory = true;
  }
  getInfo() {
    this.sold_status = false;
    this.showFullHistory = false;
    this.respond = false;
    this._api.getLotInfo(this.lot).then( result => {
      this.lotDetail = result.lot;
      if (!this.lotDetail) {
        this.router.navigate(['/'])
      }
      this.sold = result.sold;
      this.url = './assets/chart/index.html' + `?year=${this.lotDetail['info']['year']}&make=${this.lotDetail['info']['make']}&model=${this.lotDetail['info']['model']}&vin=${this.lotDetail['info']['vin']}`;
      this.changeBackground();
      this._api.getBidInfo(this.lotDetail['info']['vin']).then(result => {
        this.show_fullReports = true;
        this.winningBidDetails = result.solds;
        this.soldBidDetails = result.solds;
        this.foregoingBidDetail = result.vehicle;

        if (this.winningBidDetails.length > 1) {
          this.showDetails = true;
        } else if (this.winningBidDetails.length === 1) {
          if (this.foregoingBidDetail.length == 0) {
            this.showDetails = false;
          } else {
            this.showDetails = true;
          }
        } else {
          this.showDetails = false;
        }
        if (this.foregoingBidDetail.length > 0) {

          for (let winningBid of this.winningBidDetails) {
            if (winningBid['info']['lot'] === this.foregoingBidDetail[0]['info']['lot']) {
              if (this.winningBidDetails.indexOf(winningBid) > 0) {
                this.foregoingBidDetail = [];
                this.sold = true;
                this.lotDetail = winningBid;
              }
            }
          }
          if (this.foregoingBidDetail[0]['info']['lot'] === this.lot)
          {
            this.historyLength += 1;
          }
        }
        this.winningBidDetails.map(winningBid => {
          if (winningBid.info.lot === this.lot) {
            this.selected = this.winningBidDetails.indexOf(winningBid);
          }
        });
        this.loading = false;
        this.getPreviousBids();
      }).catch(error => {
        console.log("==========", error);
        this.loading = false;
        this.router.navigate(['/'])
      });

    }).catch( error => {
      console.log(error);
      this.router.navigate(['/'])
    })
  }

  getPreviousBids() {
    this.noAuction = false;
    this._api.getWinningBids(this.lot).then( result => {
      this.getChartData({make: this.lotDetail['info']['make'], model: this.lotDetail['info']['model'], year: this.lotDetail['info']['year']});
        let winningBids = result.solds;
        this.historyLength += winningBids.length;
        if (this.sold) {
          this.winningBids = winningBids.filter(winningBid => {
            if (winningBid['sale_date'] !== this.lotDetail['sale_date']) {
              return winningBid;
            }
          })
        } else {
          this.winningBids = winningBids;
        }
    }).catch( error => {
      console.log("-------------------", error)
      this.router.navigate(['/'])
    });
  }


  imageShow(index) {
    this.selected_image = index;
    this.changeBackground();
  }
  changeBackground() {
    const el = document.querySelector(".f_detail_main_img_a");
    const image_container = document.getElementsByClassName('detail_image')[0];
    if (el && this.lotDetail['info']) {
      el.setAttribute('style',
        `background:  url( ${this.pipe.transform(this.lotDetail.info.images, this.selected_image)});
              background-size: cover;
              background-position: center; `);
    }
  }

  ngAfterViewInit() {
    const el = document.querySelector(".f_detail_main_img_a");
    this.changeBackground();
  }

  showMoreBids() {
    this.showBids = !this.showBids;
  }
  openModal(id: string) {
      this.modalService.open(id);
  }

  closeModal(id: string) {
      this.modalService.close(id);
      this.showFullHistory = false;
  }

}
