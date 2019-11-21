import {AfterViewChecked, ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {LoaderService} from "./utils/services/loader.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewChecked{
  title = 'frontend';
  show = false;
  showLoader: boolean;

  constructor(private _loader: LoaderService, private cdRef : ChangeDetectorRef) {}

  ngOnInit(): void {
    this._loader.status.subscribe( (val: boolean) => {
      this.showLoader = val;
    })
  }
  ngAfterViewChecked(): void {
    let show = this.showLoader;
    if (show!== this.show) {
      this.show = show;
      this.cdRef.detectChanges();
    }
  }

}
