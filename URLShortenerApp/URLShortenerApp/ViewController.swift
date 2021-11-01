//
//  ViewController.swift
//  URLShortenerApp
//
//  Created by 한상혁 on 2021/10/31.
//

import UIKit


class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    // row의 개수 설정하는 메서드
    
    @IBOutlet var textfield: UITextField!
    @IBOutlet var result: UILabel!
    @IBOutlet var resultButton: UIButton!
    @IBOutlet var tableView: UITableView!
    
    var memoTitle: [String] = []
    var memoContent: [String] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // APP Background 색상 설정
        self.view.backgroundColor = UIColor(red: 244/255.0, green: 240/255.0, blue: 230/255.0, alpha: 1.0)
        // Table View Corner Round 설정
        self.tableView.layer.cornerRadius = 12.0
        // 히스토리 기록할 UserDefault 선언
        let ud = UserDefaults.standard
        if let udTitle = ud.value(forKey: "title") as? [String] {
            memoTitle = udTitle
        }
        if let udContent = ud.value(forKey: "content") as? [String]{
            memoContent = udContent
        }
        print(ud.value(forKey: "title"))
        print(ud.value(forKey: "content"))
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return memoTitle.count
    }
    // row에 나타낼 cell 설정
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as? CustomCell else {
            return UITableViewCell()
        }
        cell.labelTitle.text = memoTitle[indexPath.row]
        cell.labelContent.text = memoContent[indexPath.row]
        return cell
    }
    
    func tableView(_ tableView: UITableView, titleForDeleteConfirmationButtonForRowAt indexPath: IndexPath) -> String? {
        return "삭제"
    }
    
    // 테이블 뷰 삭제
    func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCell.EditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            let ud = UserDefaults.standard
            memoTitle.remove(at: (indexPath as NSIndexPath).row)
            ud.set(memoTitle, forKey: "title")
            memoContent.remove(at: (indexPath as NSIndexPath).row)
            ud.set(memoContent, forKey: "content")
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }
    }
    // 테이블뷰 터치 이벤트
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        textfield.text = memoTitle[(indexPath as NSIndexPath).row]
        resultButton.setTitle("\(memoContent[(indexPath as NSIndexPath).row])", for: .normal)
    }
    
    // 확인 버튼 액션
    @IBAction func ok(_ sender: Any) {
        let input_url = self.textfield.text!
        let param = "url=\(input_url)"
        let paramData = param.data(using: .utf8)
        
        // URL 객체 정의
        let url = URL(string: "http://54.180.60.55:5000/result_json")
        //let url = URL(string: "http://172.30.1.35:5000/result_json")
        // request 객체 정의
        var request = URLRequest(url: url!)
        request.httpMethod = "POST"
        request.httpBody = paramData
        request.addValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request.setValue(String(paramData!.count), forHTTPHeaderField: "Content-Length")
        
        // URLSession 객체 통해 응답값 및 처리 로직 생성
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let e = error {
                NSLog("An error has occurred:: \(e.localizedDescription)")
                return
            }
//            if let httpResponse = response as? HTTPURLResponse {
//                if httpResponse.statusCode == 404 {
//                    print("404 catch")
//                }
//            }
            // 404 ERROR 체크
            let httpResponse = response as? HTTPURLResponse
            guard httpResponse!.statusCode == 200 else {
                print("404 error")
                DispatchQueue.main.async {
                    let alert = UIAlertController(title: "URL 형식 오류", message: "http:// 또는 https://로 시작해야합니다.", preferredStyle: .alert)
                    let ok = UIAlertAction(title: "확인", style: .default)
                    alert.addAction(ok)
                    
                    self.present(alert, animated: true)
                }
                return
            }
            // 응답 처리 로직
            DispatchQueue.main.async() {
                do {
                    let object = try JSONSerialization.jsonObject(with: data!, options: []) as? NSDictionary
                    guard let jsonObject = object else { return }
                    
                    let result_url = jsonObject["url"] as? String
                    print(result_url!)
                    //self.result.text = "\(result_url!)"
                    self.resultButton.setTitle("54.180.60.55:5000/\(result_url!)", for: .normal)
                    if let title = self.textfield.text {
                        if let content = self.resultButton.currentTitle {
                            let ud = UserDefaults.standard
                            self.memoTitle.append(title)
                            ud.set(self.memoTitle, forKey: "title")
                            self.memoContent.append(content)
                            ud.set(self.memoContent, forKey: "content")
                            self.tableView.reloadData()
                        } else {
                            print("content is nil")
                        }
                    } else {
                        print("title is nil")
                    }
                } catch let e as NSError {
                    print("An error has occurred while parsing JSONObject: \(e.localizedDescription)")
                }
            }
        }
        // POST 전송
        task.resume()
    }
    // 단축링크 복사 버튼 클릭
    @IBAction func btnClick(_ sender: UIButton) {
        UIPasteboard.general.string = self.resultButton.currentTitle
    }
    
}
// 테이블 내 커스텀 셀에 대한 선언
class CustomCell: UITableViewCell {
    @IBOutlet weak var labelTitle: UILabel!
    @IBOutlet weak var labelContent: UILabel!
}
